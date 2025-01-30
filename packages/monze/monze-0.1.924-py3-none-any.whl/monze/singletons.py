import os, sys, shutil
import random
import string
from copy import deepcopy
import platform
import subprocess
from collections import OrderedDict
from pprint import pprint as ppp
from flask import current_app

from general import (
	Casting,
	Timetools,
	ListDicts,
	Pickles,
	Mainroad
)
class SyslsMeta(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]

	@classmethod
	def destroy(metacls, cls):
		if cls in metacls._instances:
			del metacls._instances[cls]

class Sysls(metaclass=SyslsMeta):
	_systempath = ''
	_sysls = [
		's_gender',

		's_origin',
		's_uni',
		's_program',

		's_year',
		's_term',
		's_lang',
		's_ec',
		's_course',
		's_stream',

		's_grading',
		's_group',
		's_status',
		's_circular',
	]
	_sysmem = dict()
	error_in_sysmem = False

	def __init__(self):
		self.init()

	def init(self):
		self._systempath = Mainroad.get_system_path()
		self._sysmem = dict()
		for syslname in self._sysls:
			d = Pickles.read(os.path.join(self._systempath, f"{syslname}.pickle"))
			if not d is None:
				self._sysmem[syslname] = self.sorteer_by_ordering(d) # OrderedDict
			else:
				self.error_in_sysmem = True
				pass
		self.make_stud_statussen()

	def is_valid(self):
		return not self.error_in_sysmem

	def sorteer_by_ordering(self, d: dict) -> OrderedDict:
		ll = list(d.values())
		ll = ListDicts.sortlistofdicts(ll, 'ordering')
		# back to id-based dict
		d = OrderedDict()
		for l in ll:
			d[l['id']] = l
		return d

	def nice_name(self, key: str):
		ss= self._sysls.copy()
		if not key in ss:
			return ''
		return key.replace('s_', '').capitalize()

	def get_lijsten_nicename(self) -> dict:
		eruit = dict()
		for sys in self._sysls.copy():
			eruit[sys] = self.nice_name(sys)
		return eruit

	def get(self):
		return deepcopy(self._sysmem)

	def get_sysl(self, syslname: str, other=False) -> OrderedDict|None:
		# gets dict with id:int as key
		if syslname in self._sysmem:
			return deepcopy(self._sysmem[syslname])

		elif other is True:
			try:
				return Pickles.read(os.path.join(self._systempath, f"{syslname}.pickle"))
			except:
				return None
		return None

	def get_sysl_as_list(self, syslname: str) -> list|None:
		if not syslname in self._sysmem:
			return None
		sd = deepcopy(self._sysmem[syslname])
		return list(sd.values())

	def get_sysl_item(self, syslname: str, id) -> any:
		try:
			id = int(id)
			return self._sysmem[syslname][id]
		except:
			return None

	def get_sysl_item_first_active(self, syslname: str) -> dict|None:
		d = self.get_sysl(syslname)
		for item in d.values():
			if item['status'] == 1:
				return item
		return None

	def set_sysl_item(self, syslname: str, id: int, value) -> bool:
		try:
			self._sysmem[syslname][id] = value
		except:
			return False
		return self.save_sysl(syslname)

	def del_sysl_item(self, syslname: str, id: int) -> bool:
		try:
			del(self._sysmem[syslname][id])
		except:
			return False
		return self.save_sysl(syslname)

	def save_sysl(self, syslname: str) -> bool:
		d = self.get_sysl(syslname)
		if d is None:
			return False
		if Pickles.write(os.path.join(self._systempath, f"{syslname}.pickle"), d):
			self.init()
			return True
		return False

	def make_sysl(self, syslname: str, d, other=False) -> bool:
		if not other and syslname not in self._sysls:
			return False
		pad = os.path.join(self._systempath, f"{syslname}.pickle")
		if Pickles.write(pad, d):
			self.init()
			return True
		return False

	def get_model(self, welk: str="") -> dict:
		model = dict(
			id = {'default': 0},
			name = {'default': ''},
			color = {'default': ''},
			extra = {'default': ''},
			status = {'default': 'actief'},
			ordering = {'default': 0},
		)
		if welk in ['s_group',]:
			model['notes'] = {'default': list()}
		return model

	def get_fields(self) -> list:
		return list(self.get_model().keys())

	def get_empty(self) -> dict:
		m = self.get_model()
		d = dict()
		for field, val in m.items():
			d[field] = val['default']
		return d

	def make_stud_statussen(self):
		# makes a list like:
		default = dict(
			registratie=[0, 10, 11, 12],
			studenten=[20],
			beoordelen=[21, 22],
			alumni=[39],
			niet=[31, 38],
			noshow=[14, 16, 18, 30],
			alle=list(range(0, 100)),
		)
		ss = self.get_sysl('s_status')
		statussen = dict(alle=list())
		for item in ss.values():
			statussen['alle'].append(item['id'])
			if item['extra'] == '' or item['extra'] == None:
				continue
			if not item['extra'] in statussen:
				statussen[item['extra']] = list()
			statussen[item['extra']].append(item['id'])
		self.stud_statussen = statussen

	def get_stud_statussen(self):
		return self.stud_statussen

class EmailsMeta(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]

	@classmethod
	def destroy(metacls, cls):
		if cls in metacls._instances:
			del metacls._instances[cls]

class Emails(metaclass=EmailsMeta):
	_emailspath = ''
	_sysmem = dict()

	def __init__(self):
		self.init()

	def init(self):
		self._emailspath = Mainroad.get_emails_path()
		self._sysmem = dict()
		if not os.path.isdir(self._emailspath):
			os.mkdir(self._emailspath)
		for fname in os.listdir(self._emailspath):
			if fname.startswith('.'):
				continue
			if not fname.endswith('.pickle'):
				continue
			d = Pickles.read(os.path.join(self._emailspath, fname))
			try:
				self._sysmem[d['name']] = d
			except:
				continue

	def make_email(self, d: dict) -> bool:
		naam = Casting.name_safe(d['name'], True)
		pad = os.path.join(self._emailspath, f"{naam}.pickle")
		if Pickles.write(pad, d):
			self.init()
			return True
		return False

	def get_single(self, naam: str) -> dict|None:
		try:
			return deepcopy(self._sysmem[naam])
		except:
			return None

	def get(self):
		return deepcopy(self._sysmem)

class ViewsMeta(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]

	@classmethod
	def destroy(metacls, cls):
		if cls in metacls._instances:
			del metacls._instances[cls]

class Views(metaclass=ViewsMeta):
	_viewspath = ''
	_defaultkey = 1723028433
	_defaultname = 'default'
	_sysmem = OrderedDict()

	def __init__(self):
		self.init()

	def empty_view(self):
		jus = UserSettings()
		return dict(
			name=self._defaultname,
			created_ts=Timetools.now_secs(),
			alias=jus.alias(),
			color='#ffffff',
			status=1,
			fields=['id', 'assessment', 'firstname', 'lastname'],
			groups=[],
			emailbuttons=[],
		)

	def void_normalize(self, view):
		empty = self.empty_view()
		nview = deepcopy(view)
		for key in empty:
			if not key in view:
				view[key] = empty[key]

	def init(self):
		self._viewspath = Mainroad.get_views_path()
		self._sysmem = OrderedDict()
		if not os.path.isdir(self._viewspath):
			os.mkdir(self._viewspath)
		for fname in os.listdir(self._viewspath):
			if fname.startswith('.'):
				continue
			if not fname.endswith('.pickle'):
				continue
			d = Pickles.read(os.path.join(self._viewspath, fname))
			key = Casting.int_(d['created_ts'], default=404)
			try:
				self._sysmem[key] = d
			except:
				continue
		if not self._defaultkey in self._sysmem:
			# nog geen standaard view 'min' in systeem:
			d = self.empty_view()
			d['created_ts'] = self._defaultkey
			self.make_view(d)

	def get_defaultkey(self) -> int:
		return self._defaultkey

	def get_defaultname(self) -> str:
		return self._defaultname

	def make_view(self, d) -> bool:
		naam = Casting.int_(d['created_ts'], True)
		pad = os.path.join(self._viewspath, f"{naam}.pickle")
		if Pickles.write(pad, d):
			self.init()
			return True
		return False

	def get(self) -> dict:
		return deepcopy(self._sysmem)

	def get_single_by_key(self, key) -> dict|None:
		try:
			return deepcopy(self._sysmem[key])
		except:
			return None

	def get_by_similar_viewname(self, groupid: int, viewid: int) -> int:
		def firstpart(viewname: str) -> str:
			viewname = viewname.replace('-', ' ').replace('_', ' ')
			return viewname.split(' ')[0].strip()

		if not viewid in self._sysmem:
			return 0
		simname = firstpart(self._sysmem[viewid]['name'])
		for k, v in self._sysmem.items():
			if not groupid in self._sysmem[k]['groups']:
				continue
			fp = firstpart(v['name'])
			if simname == fp:
				return k
		return 0

	def is_group_in_view(self, groupid: int, viewid: int) -> bool:
		if viewid == 1:
			return True
		if not viewid in self._sysmem:
			return False
		return groupid in self._sysmem[viewid]['groups']

	def is_view_active(self, viewid: int) -> bool:
		if viewid == 1:
			return True
		if not viewid in self._sysmem:
			return False
		return self._sysmem[viewid]['status'] == 1

	def get_views_by_groupid(self, groupid: int, activeonly=False) -> OrderedDict:
		g_views = OrderedDict()
		for key in self._sysmem:
			if activeonly and not self.is_view_active(key):
				continue
			if self.is_group_in_view(groupid, key):
				g_views[key] = deepcopy(self._sysmem[key])
		return g_views

	def delete(self, key: int):
		# but not if key is default view
		if key in self._sysmem and key != self._defaultkey:
			pad = os.path.join(self._viewspath, f"{key}.pickle")
			Pickles.delete(pad)
			self.init()

	def reorder_views(self, idslist: list) -> bool:
		for id in idslist:
			if not id in self._sysmem:
				continue
			self._sysmem.move_to_end(id, last=True)
		return True

	def mijn_views(self) -> list:
		jus = UserSettings()
		all = self._sysmem
		mijnviews = list()
		for key, val in all.items():
			if jus.alias() == val['alias']:
				mijnviews.append(key)
		return mijnviews

	def active_views(self, no_default=True) -> list:
		all = self._sysmem
		active = list()
		for key, val in all.items():
			if no_default and key == self.get_defaultkey():
				continue
			if self.is_view_active(key):
				active.append(val)
		return active

	def summative_views(self) -> dict:
		# returns list with active summative views
		all = self._sysmem
		active = dict()
		for key, val in all.items():
			if not self.is_view_active(key):
				continue
			if val['alias'] != "summative":
				continue
			active[key] = val
		return active

	def mijn_groepen(self, all=None) -> list:
		# groepen waarbij ik een view heb
		jus = UserSettings()
		all = self._sysmem
		mijngroepen = list()
		for key, val in all.items():
			if (jus.alias() == val['alias'] or val['alias'] == 'summative') and val['status'] > 0:
				for g in val['groups']:
					if not g in mijngroepen:
						mijngroepen.append(g)

		return mijngroepen

class StudentsMeta(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]

	@classmethod
	def destroy(metacls, cls):
		if cls in metacls._instances:
			del metacls._instances[cls]

class Students(metaclass=StudentsMeta):
	_stud_p_path = ''
	_stud_dir_path = ''
	_sysmem = dict()

	def __init__(self):
		self.init()

	def init(self):
		self._stud_p_path = Mainroad.get_studentpickles_path()
		self._stud_dir_path = Mainroad.get_student_dirs_path()
		self._sysmem = dict()
		for fname in os.listdir(self._stud_p_path):
			if fname.startswith('.'):
				continue
			if not fname.endswith('.pickle'):
				continue
			if '-LAP-' in fname:
				try:
					os.remove(os.path.join(self._stud_p_path, fname))
				except:
					pass
				continue

			d = Pickles.read(os.path.join(self._stud_p_path, fname))
			try:
				id = d['id']
				self._sysmem[id] = d
			except:
				continue

	def all(self) -> dict:
		return deepcopy(self._sysmem)

	def all_as_lod(self) -> list:
		all = self.all()
		return list(all.values())

	def active(self) -> dict:
		all = self.all()
		activelist = dict()
		for k, s in all.items():
			if s["s_status"] in [0, 10, 11, 12, 20, 21, 22]:
				activelist[k] = s
		return activelist

	def get_by_id(self, id: int) -> dict | None:
		try:
			return deepcopy(self._sysmem[id])
		except:
			return None

	def id_from_safename(self, fname: str) -> int | None:
		# sdirname = f"{lang}-{d['id']}-{first}-{last}.pickle"
		try:
			id = int(fname.split('-')[0])
			return id
		except:
			return None

	def generate_safename(self, id: int) -> str:
		return f"{id}"

	def generate_safename_full(self, id: int) -> str | None:
		d = self.get_by_id(id)
		if d is None:
			return None
		return self.generate_safename_full_from_d(d)

	def generate_safename_full_from_d(self, d: dict) -> str:
		first = Casting.name_safe(d['firstname'], False)
		last = Casting.name_safe(d['lastname'], False)
		return f"{first}-{last}-{d['id']}"

	def cleanup_before_save(self, d: dict) -> dict:
		if 'pf_url' in d:
			cont = True
			if d['pf_url'] is None:
				d['pf_url'] = ''
				# klaar
				cont = False
			if d['pf_url'] == '':
				# klaar
				cont = False

			head, sep, tail = d['pf_url'].partition('/edit')
			if cont and sep == '/edit':
				d['pf_url'] = head
				cont = False

			head, sep, tail = d['pf_url'].partition('?usp')
			if cont and sep == '?usp':
				d['pf_url'] = head
				cont = False

		# other fields

	def make_student_pickle(self, id: int, d: dict) -> bool:
		self.cleanup_before_save(d)
		try:
			ppath = os.path.join(self._stud_p_path, f"{self.generate_safename(id)}.pickle")
			Pickles.write(ppath, d)
			self.init()
		except Exception as e:
			return False
		return True

	def delete_student_pickle(self, id: int) -> bool:
		try:
			ppath = os.path.join(self._stud_p_path, f"{self.generate_safename(id)}.pickle")
			Pickles.delete(ppath)
		except Exception as e:
			return False
		self.init()
		return True

	def make_student_folder_path(self, id):
		d = self.get_by_id(id)
		if d is None:
			return None
		return self.make_student_folder_path_from_d(d)


	def make_student_folder_path_from_d(self, d):
		sysls_o = Sysls()
		if d['s_year'] < 2020:
			# print('WRONG YEAR', d['s_year'])
			return None
		if not d['s_term'] in [1, 2, 3, 4, 5, 6]:
			print('WRONG TERM', d['s_term'])
			return None
		jaar = sysls_o.get_sysl_item('s_year', d['s_year'])['name']
		term = sysls_o.get_sysl_item('s_term', d['s_term'])['name']
		safename = self.generate_safename_full_from_d(d)
		studpath = os.path.join(self._stud_dir_path, jaar, term, safename)
		return studpath

	def make_student_folder(self, id: int) -> bool:
		d = self.get_by_id(id)
		try:
			studpath = self.make_student_folder_path(id)
			if studpath is None:
				return False
		except:
			print('NO STUDENT DIR', d)
			return False
		if not os.path.isdir(studpath):
			try:
				os.makedirs(studpath, exist_ok=True)
			except Exception as e:
				return False
		return True

	def move_student_folder(self, oldpath, curpath):
		# check if old path exists
		try:
			shutil.move(oldpath, curpath)
		except:
			pass

	def new_password(self, id):
		x = ''.join(random.choices(string.ascii_lowercase+string.digits+'', k=13))
		return f"{id*13}-{x}"

	def new_student_id(self):
		newid = 0
		for i in self._sysmem:
			if newid < i:
				newid = i
		return newid + 1

	def open_student_dir(self, id):
		pad = self.make_student_folder_path(id)
		if pad is None:
			return
		self.open_dir(pad)

	def open_dir(self, pad):
		if pad is None:
			return
		try:
			if platform.system() == "Windows":
				os.startfile(pad)
			elif platform.system() == "Darwin":
				subprocess.Popen(["open", pad])
			else:
				subprocess.Popen(["xdg-open", pad])
		except Exception as e:
			pass
	def as_html(self, id):
		sysls_o = Sysls()
		d = self.get_by_id(id)
		if not isinstance(d, dict):
			print('NO STUDENT DIR', d)
			return

		studfields = list(d.keys())
		# get circular model from system
		circfields = sysls_o.get_sysl('s_circular')

		def ccolor(val: int):
			try:
				return circfields[val]['color']
			except:
				return '#eeeeee'

		def make_li(htm, label: str, waarde: str, direct=False):
			try:
				if direct:
					waarde = waarde
				else:
					waarde = d[waarde]
			except:
				waarde = ''
			return f"{htm}\n\t\t\t<li><span>{label}</span>{waarde}</li>"

		def from_list(thing):
			try:
				return sysls_o.get_sysl_item(thing, d[thing])['name']
			except:
				return ''

		def make_note(htm, note):
			try:
				notitie = note['note']
				alias = note['alias']
				dd = Timetools.ts_2_td(note['created_ts'], rev=True)
				return f"{htm}\n\t\t\t<p><span>{alias} op {dd}</span><br>{notitie}</p>"
			except:
				return f"{htm}\n\t\t\t<p><span></span></p>"

		def make_custom_old(html):
			customfields = dict() # of dicts
			try:
				for cus in d['customs'].values():
					for k, v in cus.items():
						customfields[k] = v
			except:
				pass

			if len(customfields) == 0:
				return html

			# tabel
			html = f'{html}\n\t\t\t<table class="circular">'
			# rij met kolomnamen
			html = f'{html}\n\t\t\t\t<tr>'
			for k, v in customfields.items():
				fieldname = k.replace('t_', '')
				html = f'{html}\n\t\t\t\t\t<th style="text-align: left;">{fieldname}</th>'
			html = f'{html}\n\t\t\t\t</tr>'

			# rij met cellen
			html = f'{html}\n\t\t\t\t<tr>'
			for k, v in customfields.items():
				html = f'{html}\n\t\t\t\t\t<td style="text-align: left;">{v}</td>'
			# einde rij en tabel
			html = f'{html}\n\t\t\t\t</tr>'
			html = f'{html}\n\t\t\t</table>'
			return html

		def make_custom(html, cust):
			views_o = Views()
			# creates one line for one circular
			view = views_o.get_single_by_key(cust)
			if view is None:
				return html
			viewname = view['name']

			html = f'{html}\n\t\t\t<table class="circular">'
			html = f'{html}\n\t\t\t\t<tr><th></th>'
			for field in view['fields']:
				if field in studfields:
					continue
				if not field.startswith('t_'):
					continue
				fieldname = field.replace('t_', '')
				html = f'{html}\n\t\t\t\t\t<th>{fieldname}</th>'
			html = f'{html}\n\t\t\t\t</tr>'

			html = f'{html}\n\t\t\t\t<tr><td style="width: 100px;">{viewname}</td>'
			for field in view['fields']:
				if field in studfields:
					continue
				if not field.startswith('t_'):
					continue
				if field in d['customs'][cust]:
					val = d['customs'][cust][field]
				else:
					val = ''
				# text field
				html = f'{html}\n\t\t\t\t\t<td>{val}</td>'

			html = f'{html}\n\t\t\t\t</tr>'
			html = f'{html}\n\t\t\t</table>'
			return html

		def make_circular(html, circ):
			views_o = Views()
			# creates one line for one circular
			view = views_o.get_single_by_key(circ)
			if view is None:
				return html
			viewname = view['name']

			html = f'{html}\n\t\t\t<table class="circular">'
			html = f'{html}\n\t\t\t\t<tr><th></th>'
			for field in view['fields']:
				if field in studfields:
					continue
				if not field.startswith('c_'):
					continue
				fieldname = field.replace('c_', '')
				html = f'{html}\n\t\t\t\t\t<th>{fieldname}</th>'
			html = f'{html}\n\t\t\t\t</tr>'

			html = f'{html}\n\t\t\t\t<tr><td style="width: 100px;">{viewname}</td>'
			for field in view['fields']:
				if field in studfields:
					continue
				if not field.startswith('c_'):
					continue
				if field in d['circulars'][circ]:
					val = d['circulars'][circ][field]
				else:
					val = 0
				# kleurveld
				kleur = ccolor(val)
				html = f'{html}\n\t\t\t\t\t<td style="background-color: {kleur}"></td>'

			html = f'{html}\n\t\t\t\t</tr>'
			html = f'{html}\n\t\t\t</table>'
			return html

		# ======= main van de html def =======
		if d is None:
			return
		if d['s_status'] in [39]:  # passed
			kleur = 'dodgerblue'
		elif d['s_status'] in [10, 11, 12]:  # ingeschreven
			kleur = 'rgb(254, 232, 86)'  # geel
		elif d['s_status'] in [20, 21, 22]:  # bezig
			kleur = 'darkgreen'
		elif d['s_status'] in [30, 31, 38]:  # gezakt oid
			kleur = 'rgb(221, 53, 110)'  # signaal
		else:
			kleur = "#eee"

		html = self.basic_student_html() % (d['firstname'], d['lastname'], kleur, kleur, id, d['firstname'], d['lastname'])

		# velden
		html = make_li(html, 'Voornaam', 'firstname')
		html = make_li(html, 'Achternaam', 'lastname')
		html = make_li(html, 'Groep', from_list('s_group'), direct=True)
		html = make_li(html, 'Email', 'email')
		html = make_li(html, 'MVO', from_list('s_gender'), direct=True)

		try:
			url = d["pf_url"]
			link = f'<a href="{url}">{url}</a>'
		except:
			url = ''
			link = ''
		html = make_li(html, 'portfolio', link, direct=True)

		html = make_li(html, 'Wachtwoord', 'password')
		html = make_li(html, 'Cijfer', 'grade')

		if d['grade'] < 1:
			datum = ''
		else:
			try:
				datum = Timetools.ts_2_td(d['grade_ts'], rev=True)
			except:
				datum = ''
		html = make_li(html, 'Cijferdatum', datum, direct=True)

		html = make_li(html, 'Status', from_list('s_status'), direct=True)
		html = make_li(html, 'Herkomst', from_list('s_origin'), direct=True)
		html = make_li(html, 'Uni', from_list('s_uni'), direct=True)
		html = make_li(html, 'Programma', from_list('s_program'), direct=True)
		html = make_li(html, 'Jaar', from_list('s_year'), direct=True)
		html = make_li(html, 'Periode', from_list('s_term'), direct=True)
		html = make_li(html, 'Minor', from_list('s_course'), direct=True)
		html = make_li(html, 'ECs', from_list('s_ec'), direct=True)
		html = make_li(html, 'Taal', from_list('s_lang'), direct=True)

		html = make_li(html, 'KOM-code', 'kom_code')
		html = make_li(html, 'NHLS-code', 'nhls_code')

		html = f'{html}\n\t\t</ul>\n\t\t<h2>Custom fields</h2>\n\t\t<div class="customs">'
		if 'customs' in d:
			for cust in d['customs']:
				html = make_custom(html, cust)

		html = f'{html}\n\t\t</div>\n\t\t<h2>Checks</h2>\n\t\t<div class="circulars">'
		if 'circulars' in d:
			for circ in d['circulars']:
				html = make_circular(html, circ)

		html = f'{html}\n\t\t</div>\n\t\t<h2>Notities</h2>\n\t\t<div class="notes">'
		if 'notes' in d:
			for note in d['notes']:
				html = make_note(html, note)

		html = f'{html}\n\t\t</div>\n\t</body>\n</html>'
		filename = self.generate_safename_full_from_d(d) + '.html'
		dirpath = self.make_student_folder_path_from_d(d)
		filepath = os.path.join(dirpath, filename)
		# print('HTML', filepath)
		with open(filepath, 'w') as f:
			f.write(html)

	def basic_student_html(self):
		return '''<!DOCTYPE html>
	<html lang="en">
		<head>
			<title>%s %s</title>
			<style>
				*{
					font-family: Arial, Helvetica, sans-serif;
					font-size: 14px;
					border-radius: 3px;
				}
				body{
					padding: 1em;
				}
				ul{
					list-style: inside;
	                list-style-type: none;
	                margin: 0;
	                border: 2px solid %s;
					padding: 1em;
	            }
	            li{
	                margin: 0 0 0.5em 0;
	                padding: 0;
	                border-bottom: 1px solid #ddd;
	            }
	            li span{
	                display: inline-block;
	                width: 10em;
	                font-size: 0.8em;
	            }
	            div.notes,
	            div.circulars,
	            div.customs{
	                margin: 1em 0 0 0;
	                border: 2px solid %s;
					padding: 1em;
	            }
	            p span{
	                border-bottom: 1px solid #ddd;
	                font-size: 0.8em;
	            }
	            .circular{
	                overflow: hidden;
					white-space: nowrap;
	            }
	            .circular td,
	            .circular th{
	                font-size: 0.8em;
	                padding: 0.25em 0.5em;
	            }
	
			</style>
		</head>
		<body>
			<h1>%s %s %s</h1>
			<ul>
	'''

class UserSetingsMeta(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]

	@classmethod
	def destroy(metacls, cls):
		if cls in metacls._instances:
			del metacls._instances[cls]
class UserSettings(metaclass=UserSetingsMeta):
	_props = dict()
	# ROLLEN 'beheer', 'docent', 'administratie', 'admin'

	# sysls leeft in app, leest/schrijft niet zelf props
	# mainroad leeft in monze, leest schrijft settings
	# props in sysl == settings in mainroad.
	def __init__(self):
		self.read_props()

	def version(self):
		return Mainroad.get_version()

	def _is(self) -> bool:
		# check if this user has user settings
		try:
			if not 'alias' in self._props or not 'magda' in self._props:
				self.logoff()
				return False
			# known user with settings and login in own computer
			return True
		except:
			self.logoff()
			return False

	def is_new(self):
		return self.get_prop("isnew", default=True)

	def alias(self):
		return self.get_prop("alias", default="stranger")

	def _alias(self):
		return self.alias()

	def odpad(self):
		return self.get_prop("onedrive", default=None)

	def settingspad(self):
		return Mainroad.get_settings_path()

	def magda(self, rol: list, alias: str = None) -> bool:
		# alias is de alias van het ding
		rollen = self.get_prop("magda", default=[])
		if 'admin' in rollen:
			return True
		damag = len(list(set(rol) & set(rollen))) > 0
		if not alias is None:
			damag = damag and alias.strip() == self.alias()

		return damag

	def get_prop(self, key: str, default=None):
		try:
			return self._props[key]
		except:
			return default

	def _prev(self) -> str:
		try:
			return self._props['prev_url']
		except:
			return ''

	def set_prop(self, key: str, val):
		# normalize
		if not key in Mainroad.get_empty_settings():
			return
		self._props[key] = val  # update or create
		Mainroad.set_settings(self._props)

	def read_props(self):
		self._props = Mainroad.get_settings()

	def get_props(self):
		return self._props

	def set_props(self, d: dict):
		# normalize props
		newsettings = Mainroad.get_empty_settings()
		for e in newsettings:
			if e in d:
				newsettings[e] = d[e]
			else:
				# default val
				pass
		self._props = newsettings
		Mainroad.set_settings(self._props)

	def get_searchterms(self) -> list:
		try:
			return self.get_prop('searchterms', default=[])
		except:
			return []

	def add_searchterm(self, st: str) -> list:
		current = self.get_searchterms()
		if st in current:
			return current
		current.insert(0, st)
		current = current[:10]
		self.set_prop('searchterms', current)
		Mainroad.set_settings(self._props)
		return current


	def set_sort(self, path, field, direction):
		# sets sorting for specific path
		# as list with two values: fieldname and direction asc, desc
		sorting = self.get_prop('sorting', default={})
		sorting[path] = [path, field, direction]
		self.set_prop('sorting', sorting)


	def get_sort(self, path) -> list|None:
		sorting = self.get_prop('sorting', default={})
		try:
			return sorting[path]
		except:
			return []

