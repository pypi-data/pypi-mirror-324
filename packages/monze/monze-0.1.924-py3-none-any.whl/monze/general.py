import bleach
from datetime import datetime
import pytz
import time
import pathlib
import os
from urllib.parse import quote_plus as kwoot
import re
import pickle
import sys
from pprint import pprint as ppp
from ftplib import FTP
import io
import appdirs
from colorama import Fore, Style, Back
import requests

class Css:
	# uses colorama for creating style in prompt
	@classmethod
	def reset(cls) -> str:
		return f" {Style.RESET_ALL}"

	@classmethod
	def normal(cls) -> str:
		return f"{Style.NORMAL}"

	@classmethod
	def bold(cls) -> str:
		return f"{Style.BRIGHT}"

	@classmethod
	def good(cls) -> str:
		return f"{Back.LIGHTGREEN_EX}{Fore.BLACK}{Style.BRIGHT} "

	@classmethod
	def warn(cls) -> str:
		return f"{Back.LIGHTCYAN_EX}{Fore.BLACK}{Style.BRIGHT} "

	@classmethod
	def att(cls) -> str:
		# more serious than warn
		return f"{Back.LIGHTYELLOW_EX}{Fore.BLACK}{Style.BRIGHT} "

	@classmethod
	def wrong(cls) -> str:
		return f"{Back.LIGHTRED_EX}{Fore.BLACK}{Style.BRIGHT} "

	@classmethod
	def prompt(cls) -> str:
		return f"{Fore.BLACK}{Style.BRIGHT} "

	@classmethod
	def log(cls) -> str:
		return f"{Fore.MAGENTA}{Style.NORMAL} "


class Pickles:
	@classmethod
	def read(cls, path: str) -> any:
		try:
			return pickle.load(open(path, 'rb'))
		except Exception as e:
			pass
			# print('Pickles.read', e)
		return None

	@classmethod
	def write(cls, path: str, d: dict|list) -> bool:
		dirpath = os.path.dirname(path)
		if not os.path.isdir(dirpath):
			os.makedirs(dirpath)
		try:
			pickle.dump(d, open(path, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
			return True
		except Exception as e:
			print('Pickles.write', e)
		return False

	@classmethod
	def delete(cls, path: str) -> bool:
		try:
			os.remove(path)
			return True
		except:
			return False


class Mainroad:
	forca = list()
	version = ''
	devdev = False
	logging = False
	speedup = False
	updateurl = 'cpnits.com/butterfly.html'
	settingspickle = "butterfly2.pickle"
	browser = None

	@classmethod
	def get_empty_settings(cls) -> dict:
		return dict(
			onedrive='',
			magda=['docent'],
			alias='',
			password='',
			version=cls.version,
			logging=False,
			searchterms = [],
			prev_url = '',
			last_url = '',
			isnew = True,
			sorting = [],
		)

	@classmethod
	def get_version(cls):
		return cls.version

	@classmethod
	def delete_settings(cls):
		settings_path = cls.get_settings_path()
		try:
			os.remove(settings_path)
		except:
			pass

	@classmethod
	def toggle_logging(cls):
		cls.logging = not cls.logging
		print('cls.logging', cls.logging)
		props = cls.get_settings()
		props['logging'] = cls.logging
		cls.set_settings(props)

	@classmethod
	def test_settings(cls) -> bool:
		# checks if settingsfile is ok
		settings_path = cls.get_settings_path()
		thing = Pickles.read(settings_path)
		if thing is None:
			cls.loglog(f"{Css.wrong()}no thing 0: {thing}")
			return False

		# thing should contain proper settings
		if not isinstance(thing, dict):
			cls.loglog(f"{Css.wrong()}test_settings_thing 1: {thing}{Css.reset()}")
			return False
		if not 'onedrive' in thing:
			cls.loglog(f"{Css.wrong()}test_settings_thing 2: no onedrive in {thing}{Css.reset()}")
			return False
		if not os.path.isdir(thing['onedrive']):
			cls.loglog(f"{Css.wrong()}test_settings_thing 6: OneDrive not valid in {thing}{Css.reset()}")
			return False
		if cls.get_setting("alias") == '' or cls.get_setting("alias") is None:
			cls.loglog(f"{Css.wrong()}test_settings_thing 4: na alias in {thing}{Css.reset()}")
			return False
		if cls.get_setting("password") == '' or cls.get_setting("password") is None:
			cls.loglog(f"{Css.wrong()}test_settings_thing 5: no password in {thing}{Css.reset()}")
			return False
		return True

	@classmethod
	def get_message(cls, newline=' ') -> str|None:
		path = os.path.join(cls.get_onedrive_path(), 'DO_NOT_DELETE.txt')
		try:
			lines = list()
			with open(path, 'r') as f:
				lines = f.readlines()
			return newline.join(lines)
		except:
			return None

	@classmethod
	def force_reset(cls):
		settingspath = cls.get_settings_path()
		try:
			os.remove(settingspath)
		except:
			pass

	@classmethod
	def try_to_login(cls, password: str, odpath: str) -> dict|None:
		upath = os.path.join(odpath, 'system', 's_srs.pickle')
		users = Pickles.read(upath)
		if users is None:
			sys.exit(f"{Css.wrong()}No valid mainroad to _BUTTERFLY{Css.reset()}")
		for u in users: # users is list
			if u['password'].strip() == password:
				return u
		return None

	@classmethod
	def login(cls, newuser: dict):
		cls.set_settings(newuser)

	# not in use
	@classmethod
	def force_access(cls, name, accessdir):
		if name in cls.forca:
			return

		if name == 'settings':
			try:
				os.makedirs(accessdir, exist_ok=True)
			except Exception as e:
				cls.loglog(f"{Css.wrong()}Force access to dir [{accessdir}] failed.\n\t e = {e}")
				sys.exit(f"{Css.wrong()}Force access to dir [{accessdir}] failed.{Css.reset()}\n\t e = {e}")

		try:
			with open(os.path.join(accessdir, 'access.txt'), 'w') as f:
				cls.loglog(f"Forcing access to [{name}] \n\t{accessdir} \n\t@ {Timetools.now_string()}")
				cls.forca.append(name)
		except Exception as e:
			sys.exit(f"{Css.wrong()}Force access to [{name}] failed.{Css.reset()}\n\t e = {e}")
		try:
			pass
			os.remove(os.path.join(accessdir, 'access.txt'))
		except:
			pass
		cls.loglog(f"Force access to [{name}] GELUKT")


	@classmethod
	def exit_message(cls, message: str):
		# sys.exit(message)
		print(message)

	@classmethod
	def get_settings_dir(cls) -> str:
		sd = appdirs.user_config_dir()
		if not os.path.isdir(sd):
			sys.exit(f'{Css.wrong()}Bizar. Your computer has no {sd} path.{Css.reset()}')
		return os.path.join(appdirs.user_config_dir(), 'JeexButterfly')

	@classmethod
	def get_settings_path(cls) -> str:
		# no testing involved
		settings_dir = cls.get_settings_dir()
		settings_path = os.path.join(settings_dir, cls.settingspickle)
		return settings_path

	@classmethod
	def get_desktop_path(cls) -> str:
		try:
			desktop = os.path.join(pathlib.Path.home(), 'Desktop')
			return desktop
		except Exception as e:
			return ''

	@classmethod
	def get_onedrive_path(cls, firstrun: bool = False) -> str|None:
		# only for use after first init.
		settings_path = cls.get_settings_path()
		settings = Pickles.read(settings_path)
		if settings is None:
			if not firstrun:
				sys.exit(f'{Css.wrong()}ERROR: No Settings found [1].{Css.reset()}')
			return None
		try:
			return settings['onedrive']
		except:
			# geen onedrive in settings
			sys.exit(f'{Css.wrong()}ERROR: No OneDrive found [2].{Css.reset()}')

	@classmethod
	def get_system_path(cls):
		return os.path.join(cls.get_onedrive_path(), 'system')

	@classmethod
	def get_emails_path(cls):
		return os.path.join(cls.get_onedrive_path(), 'emails')

	@classmethod
	def get_views_path(cls):
		return os.path.join(cls.get_onedrive_path(), 'views')

	@classmethod
	def get_studentpickles_path(cls):
		return os.path.join(cls.get_onedrive_path(), 'students')

	@classmethod
	def get_student_dirs_path(cls):
		# is dir up from onedrive_path / _JAREN
		upper = os.path.dirname(cls.get_onedrive_path())
		return os.path.join(upper, '_JAREN')

	@classmethod
	def get_setting(cls, name: str):
		try:
			props = cls.get_settings()
			return props[name]
		except:
			return None

	@classmethod
	def get_settings(cls) -> dict | None:
		try:
			propspad = cls.get_settings_path()
			props = Pickles.read(propspad)
			return props
		except:
			return None

	@classmethod
	def set_setting(cls, name: str, value: any):
		props = cls.get_settings()
		if props is None:
			return
		props[name] = value
		cls.set_settings(props)

	@classmethod
	def set_settings(cls, props: dict):
		propspad = cls.get_settings_path()
		try:
			Pickles.write(propspad, props)
		except Exception as e:
			pass

	@classmethod
	def set_new_settings(cls, odpath: str):
		props = cls.get_empty_settings()
		props["onedrive"] = odpath
		cls.set_settings(props)

	@classmethod
	def loglog(cls, t: str):
		cls.logging = cls.get_setting('logging')
		if cls.logging:
			print(f"{Css.log()}t{Css.reset()}")


class Startup:
	# this is before initialising or starting Flask app
	@classmethod
	def optionals(cls, args):
		browsers = [
			"mozilla",
			"firefox"
			"epiphany",
			"kfmclient",
			"konqueror",
			"kfm",
			"opera",
			"links",
			"elinks",
			"lynx",
			"w3m",
			"windows-default",
			"macosx",
			"safari",
			"chrome",
			"chromium",
			"chrome",
			"chromium-browser",
			"iosbrowser",
		]
		Mainroad.browser = Mainroad.get_setting("browser")
		if '--version' in args:
			sys.exit(f"Monze version: {Mainroad.get_version()}")
		if '--logoff' in args:
			Mainroad.delete_settings()
			sys.exit(f"User settings deleted. Restart server")
		if '--logging' in args:
			Mainroad.logging = True
		if '--speedup' in args:
			Mainroad.speedup = True
		for b in browsers:
			if f"--{b}" in args:
				Mainroad.browser = b
				break
	@classmethod
	def check_version(cls):
		githuburl = "https://raw.githubusercontent.com/jeex/jeex_public/refs/heads/main/monze_version.txt"
		r = requests.get(githuburl)
		if r.status_code == 200:
			monze_version = r.content.decode("utf-8").strip()
			if monze_version > Mainroad.get_version():
				sys.exit(
					f"{Css.warn()}This version is {Mainroad.get_version()}. Upgrade with newer version {monze_version} with: {Css.reset()}\n\tpip install monze --upgrade")

	@classmethod
	def get_odpath(cls) -> str:
		odpath = Mainroad.get_onedrive_path(firstrun=True)
		while odpath is None:
			print(
				f"{Css.warn()}You have to assign the _BUTTERFLY folder. Return = Cancel.{Css.reset()}")
			# root = tk.Tk()
			# root.withdraw()
			# odpath = filedialog.askdirectory(title='Open OneDrive dir _BUTTERFLY')
			odpath = input(f"{Css.prompt()}Path:{Css.reset()}").strip()
			# filtering out Onedrive path stuff
			odpath = odpath.replace(r"\ -", r" -").replace(r"-\ ", r"- ").replace('"', '')
			if odpath is None:
				sys.exit(f'{Css.good()}Exit with Cancel.{Css.reset()}')
			if len(odpath) == 0:  # cancel
				sys.exit(f'{Css.good()}Exit with Cancel.{Css.reset()}')

			if odpath.strip() == '':
				print(f'{Css.wrong()}This is an empty path [empty].{Css.reset()}')
				odpath = None

			if not odpath.endswith('_BUTTERFLY'):
				print(
					f'{Css.wrong()}This path {odpath} is not a working path to _BUTTERFLY [_BUTTERFLY].{Css.reset()}')
				odpath = None
			# correct path, test it, EXIT if wrong
			# Mainroad.force_access('onedrive', odpath)
			if not odpath is None:
				if not os.path.isdir(odpath):
					print(
						f'{Css.wrong()}This is path {odpath} not a working path to _BUTTERFLY [isdir].{Css.reset()}')
					odpath = None

			if not odpath is None:
				print(f"{Css.good()}{odpath} is OK.{Css.reset()}")
		return odpath

	@classmethod
	def check_settings(cls, odpath: str):
		retry = False
		while not Mainroad.test_settings():
			# remove settings file because it contains errors
			Mainroad.delete_settings()
			# start new
			if retry:
				print(f"{Css.wrong()}Login Failed, try again.{Css.reset()}", flush=True)
			else:
				print(f"{Css.warn()}You have to login. Return == Cancel.{Css.reset()}")
			# root = tk.Tk()
			# root.withdraw()
			# pw = simpledialog.askstring("Input", "Enter your password")
			pw = input(f"{Css.prompt()}Password:{Css.reset()}")
			if pw is None:  # cancel
				sys.exit(f'{Css.good()} Exit with Cancel.{Css.reset()}')
			if len(pw) == 0:  # cancel
				sys.exit(f'{Css.good()} Exit with Cancel.{Css.reset()}')

			pw = pw.strip()
			user = Mainroad.try_to_login(pw, odpath)
			if user is None:
				print(f"{Css.wrong()}No valid login: {pw}.{Css.reset()}")
				continue
			# set usersettings in user's pc
			newuser = Mainroad.get_empty_settings()
			newuser["onedrive"] = odpath
			newuser["magda"] = user["magda"]
			newuser["alias"] = user["alias"]
			newuser["password"] = pw
			newuser["version"] = Mainroad.version,
			newuser["logging"] = False

			# log user in and make settings file
			Mainroad.login(newuser)
			retry = True

		# finished logging in with success
		if retry:
			print(f"{Css.good()}Login OK.{Css.reset()}", flush=True)
		else:
			print(f"{Css.good()}Automatic login OK.{Css.reset()}", flush=True)

		# change settings from prompt
		Mainroad.set_setting("browser", Mainroad.browser)
		Mainroad.set_setting("logging", Mainroad.logging)


class BaseClass:
	@classmethod
	def get_model(cls) -> dict:
		return dict()

	@classmethod
	def get_empty(cls) -> dict:
		m = cls.get_model()
		newm = dict()
		for key, val in m.items():
			newm[key] = val['default']
		return newm


# General function for type casting
class Casting:
	@classmethod
	def name_safe(cls, s: str, nums: bool) -> str:
		# removes all none-word chars
		parts = s.replace('-', ' ').split(' ')
		nieuw = []
		for p in parts:
			if nums:
				p = re.sub(r'[^a-zA-Z0-9_]', '', p, count=1000).lower().strip()
			else:
				p = re.sub(r'[^a-zA-Z_]', '', p, count=1000).lower().strip()
			if p != '':
				nieuw.append(p)
		return '-'.join(nieuw)

	@classmethod
	def str_(cls, erin, default: str|None='') -> str|None:
		try:
			return str(erin)
		except:
			return default

	@classmethod
	def int_(cls, erin, default: int|None=0) -> int|None:
		try:
			return int(erin)
		except:
			return default

	@classmethod
	def float_(cls, erin, default=0.0) -> float:
		try:
			return float(erin)
		except:
			return default

	@classmethod
	def bool_(cls, erin, default=True) -> bool:
		try:
			return bool(erin)
		except:
			return default

	@classmethod
	def listint_(cls, erin, default=[]):
		try:
			for i in range(len(erin)):
				erin[i] = int(erin[i])
			return erin
		except:
			return default

	@classmethod
	def liststr_(cls, erin, default=[]):
		try:
			for i in range(len(erin)):
				erin[i] = str(erin[i])
			return erin
		except:
			return default

	@classmethod
	def cast(cls, erin, intotype, default=None) -> any:
		if intotype == int:
			if default is None:
				return cls.int_(erin)
			else:
				return cls.int_(erin, default=default)
		elif intotype == float:
			if default is None:
				return cls.float_(erin)
			else:
				return cls.float_(erin, default=default)
		elif intotype == bool:
			if default is None:
				return cls.bool_(erin)
			else:
				return cls.bool_(erin, default=default)
		return str(erin).strip()

	@classmethod
	def typecast_list(cls, l: list, t: type) -> list:
		try:
			return list(map(t, l))
		except Exception as e:
			return []


# General functions for working with time
class Timetools:
	TTIMESTRING = "%Y%m%dT%H00"
	DATETIME_LOCAL = "%Y-%m-%dT%H:%M"
	DATETIMESTRING = "%Y-%m-%d %H:%M:%S"
	DATETIMESTRING_NL = "%d-%m-%Y %H:%M:%S"
	DATESTRING = "%Y-%m-%d"
	DATESTRING_NL = "%d-%m-%Y"
	BIRTH = '1972-02-29'

	# TODO zorgen dat altijd de juiste NL tijd is.

	@classmethod
	def dtlocal_2_ts(cls, tts: str):
		try:
			dt = datetime(
				year=int(tts[0:4]),
				month=int(tts[5:7]),
				day=int(tts[8:10]),
				hour=int(tts[11:13]),
				minute=int(tts[14:16])
			)
			return int(dt.timestamp())
		except:
			return Timetools.td_2_ts(cls.BIRTH)

	@classmethod
	def dtonixzips_2_tms(cls, tts: str):
		try:
			dt = datetime(
				year=int(tts[0:4]),
				month=int(tts[5:7]),
				day=int(tts[8:10]),
				hour=int(tts[11:13]),
				minute=int(tts[14:16]),
				second=int(tts[17:19]),
				microsecond=int(tts[20:])
			)
			return int(dt.timestamp() * 1000)
		except Exception as e:
			return Timetools.td_2_ts(cls.BIRTH) * 1000

	@classmethod
	def td_2_ts(cls, datum: str) -> int:
		# convert date-string yyyy-mm-dd to seconds timestamp
		try:
			dt = datetime(
				year=int(datum[0:4]),
				month=int(datum[5:7]),
				day=int(datum[8:10]),
			)
			return int(dt.timestamp())
		except:
			return Timetools.td_2_ts(cls.BIRTH)

	@classmethod
	def tdtime_2_ts(cls, datumtijd: str) -> int:
		# convert date-string yyyy-mm-dd to seconds timestamp
		try:
			dt = datetime(
				year=int(datumtijd[0:4]),
				month=int(datumtijd[5:7]),
				day=int(datumtijd[8:10]),
				hour=int(datumtijd[11:13]),
				minute=int(datumtijd[14:16]),
				second=int(datumtijd[17:19]),
			)
			return int(dt.timestamp())
		except:
			return Timetools.td_2_ts(cls.BIRTH)

	@classmethod
	def ts_2_td(cls, timest: int, rev=False, withtime=False, local=False) -> str:
		# convert seconds to datestring yyyy-mm-dd
		if local:
			dstr = cls.DATETIME_LOCAL
		elif withtime:
			if rev:
				dstr = cls.DATETIMESTRING
			else:
				dstr = cls.DATETIMESTRING_NL
		else:
			if rev:
				dstr = cls.DATESTRING
			else:
				dstr = cls.DATESTRING_NL
		try:
			return datetime.fromtimestamp(timest, pytz.timezone("Europe/Amsterdam")).strftime(dstr)
		except:
			return ''

	@classmethod
	def now(cls) -> float:
		return time.time()

	@classmethod
	def now_secs(cls) -> int:
		# for normal use
		return int(cls.now())

	@classmethod
	def now_milisecs(cls) -> int:
		# for use in generating unique numbers
		return int(cls.now() * 1000)

	@classmethod
	def now_nanosecs(cls) -> int:
		# not preferred
		return int(cls.now() * 1000000)

	@classmethod
	def ts_2_datetimestring(cls, ts: int|float|None, rev=False, noseconds=False):
		if rev:
			dstr = cls.DATETIMESTRING
		else:
			dstr = cls.DATETIMESTRING_NL
		if noseconds:
			dstr = dstr[:-3]
		if ts is None:
			ts = cls.now()
		if isinstance(ts, int):
			if len(str(ts)) > 11:
				ts = ts / 1000 # nanoseconds
		if not isinstance(ts, float):
			ts = Casting.float_(ts, 0) # adding trailing zero's representing ms and ns
		return datetime.fromtimestamp(ts, pytz.timezone("Europe/Amsterdam")).strftime(dstr)

	@classmethod
	def ts_2_datestring(cls, ts: int | float | None, rev=False):
		if rev:
			dstr = cls.DATESTRING
		else:
			dstr = cls.DATESTRING_NL

		if ts is None:
			ts = cls.now()
		if isinstance(ts, int):
			if len(str(ts)) > 13:
				ts = ts / 1000000  # nanoseconds
			elif len(str(ts)) > 11:
				ts = ts / 1000  # milliseconds
		if not isinstance(ts, float):
			ts = Casting.float_(ts, 0)  # adding trailing zero's representing ms and ns
		return datetime.fromtimestamp(ts, pytz.timezone("Europe/Amsterdam")).strftime(dstr)

	@classmethod
	def now_string(cls) -> str:
		return datetime.fromtimestamp(cls.now(), pytz.timezone("Europe/Amsterdam")).strftime(cls.DATETIMESTRING)
		# return str(datetime.strptime(timestamp, cls.DATETIMESTRING))

	@classmethod
	def datetimenow(cls):
		return datetime.now()

	@classmethod
	def draaiom(cls, erin):
		# changes yyyy-mm-dd into dd-mm-yyyy and vv
		try:
			d = erin.split('-')
			return f'{d[2]}-{d[1]}-{d[0]}'
		except:
			return erin

	@classmethod
	def sleep(cls, s: float):
		time.sleep(s)


# General functions for List and Dict manipulation
class ListDicts:
	@staticmethod
	def is_intersect(a: list, b: list) -> bool:
		# returns if values in a are also in b
		try:
			return len(set(a) & set(b)) > 0
		except:
			return False

	@staticmethod
	def all_a_in_b(needles: list, haystack: list) -> bool:
		# checks if all items a are in b.
		# a is the list with required items, b is the list to be checked
		for item in needles:
			if not item in haystack:
				return False
		return True

	@staticmethod
	def sortlistofdicts(lijst: list, sleutel: str|int, reverse=False) -> list:
		try:
			return sorted(lijst, key=lambda d: d[sleutel], reverse=reverse)
		except:
			return lijst


class IOstuff:
	@classmethod
	def make_empty_record(cls, model: dict) -> dict:
		empty = dict()
		for key in model:
			empty[key] = model[key]['default']
		return empty

	# ----------------- cleaning input -----------------
	@classmethod
	def normalize(cls, d: dict, empty_record: dict):
		normalized = dict()
		for key in empty_record:
			if key in d:
				normalized[key] = d[key]
			else:
				normalized[key] = empty_record[key]
		return normalized

	@classmethod
	def normalize_keys(cls, record, emptyrecord) -> dict:
		return cls.normalize(record, emptyrecord)

	@classmethod
	def check_required_keys(cls, keys, reqlist) -> bool:
		# IMP ALWAYS run this before running other defs
		# checks if all required fields are in form
		return ListDicts.all_a_in_b(reqlist, keys)

	@classmethod
	def sanitize(cls, erin):
		return cls.bleken(erin, tags=[])

	@classmethod
	def bleken(cls, erin, tags=[]):
		try:
			erin = bleach.clean(erin, tags=tags, strip=True, strip_comments=True)
		except:
			pass
		if not isinstance(erin, str):
			return ''
		elif erin in ['None', 'none', 'null', 'Null']:
			erin = ''
		return erin

	@classmethod
	def crunch_singles(cls, requestdata, keys) -> dict|None:
		# returns None if key not exists
		result = dict()
		for key in keys:
			try:
				result[key] = cls.sanitize(requestdata[key])
			except:
				return None
		return result

	@classmethod
	def crunch_multi(cls, vals, key) -> list:
		# returns empty list if key not exists
		try:
			for i in range(len(vals)):
				vals[i] = cls.sanitize(vals[i])
			return vals
		except:
			return list()

	# ------------- generic object functions ---------
	@classmethod
	def get_lijst(cls, lijstname: str) -> dict:
		pass
		'''try:
			return lijsten.get_lijst(lijstname)
		except:
			return dict()
'''
	# ------------- ajax functions ----------------
	@classmethod
	def ajaxify(cls, a: any) -> any:
		def iterate_list(l: list) -> list:
			for i in range(len(l)):
				if isinstance(l[i], dict):
					l[i] = iterate_dict(l[i])
				elif isinstance(l[i], list):
					l[i] = iterate_list(l[i])
				else:
					# single value
					pass
			return l
		def iterate_dict(d: dict) -> dict:
			for key in d.keys():
				if isinstance(d[key], dict):
					d[key] = iterate_dict(d[key])
				elif isinstance(d[key], list):
					d[key] = iterate_list(d[key])
				else:
					# single value
					pass
			return d
		if isinstance(a, list):
			a = iterate_list(a)
		elif isinstance(a, dict):
			a = iterate_dict(a)
		# single type value
		else:
			pass
		return a


# ======= as object embedded with data for jinja only =========
class JINJAstuff:
	record = dict()
	model = dict()
	def __init__(self, record, model):
		self.record = record
		self.model = model
		self.lijsten = None # lijsten

	def __del__(self):
		pass

	# ------------- jinja functions only ----------------
	def _id(self):
		try:
			return self.record['id']
		except:
			return ''

	def _kwoot(self, erin):
		# also removes double spaces
		erin = re.sub(' +', ' ', erin)
		return kwoot(erin, safe='', encoding='utf-8', errors='replace')

	def _get_lijst(self, lijstname: str) -> dict:
		try:
			return self.lijsten.get_lijst(lijstname)
		except:
			return dict()

	def _has(self, key) -> bool:
		# key is in record
		return key in self.record

	def _is(self, key: str, val: any) -> bool:
		# compares given val with key-val in current record
		if val is None:
			return False
		return val == self.record[key]

	def _in(self, record_key: str, needle: any) -> bool:
		# checks if give value is in val (list, str, dict)
		try:
			return needle in self.record[record_key]
		except:
			return False

	def _try(self, key, default: any = '') -> any:
		# gets a key from an object if possible
		try:
			return self.record[key]
		except:
			return default

	def _trydeeper(self, key, deepkey, default: any=''):
		one = self._try(key, default=default)
		try:
			return one[deepkey]
		except:
			return one

	def _try_l(self, key, default: any = '') -> any:
		# tries to get value from connected Lijst, if not, default
		val = self._try(key, default=None)  # value from record
		if self.model is None or val is None:
			return default

		try:
			sysl = self.model[key]['lijst']  # name of lijst from lijsten module
			de_lijst = self._get_lijst(sysl)
			return de_lijst[val]
		except:
			return default

	def _bleach(self, key, default='') -> str:
		# bleach flaptext
		tekst = self._try(key, default='')
		try:
			return bleach.clean(
				tekst,
				tags={'b', 'i', 'em', 'br', 'strong', 'small', 'h1', 'h2', 'h3', 'h4', 'h5'},
			    attributes={},
				protocols={},
				strip=True,
				strip_comments=True
			)
		except:
			return ''

	def set_flash(self, key: str, msg: str):
		if not hasattr(self, 'flashes'):
			self.flashes = dict()
		self.flashes[key] = msg

	# with jinja-object giving feedback
	def get_flash(self, key) -> str:
		try:
			return f'<p class="flashed" data-flash="{key}">{self.flashes[key]}</p>'
		except:
			return ''

	def mark_flash(self, key):
		try:
			if key in self.flashes:
				return ' mark-input '
		except:
			pass
		return ''

	def get_record(self):
		return self.record


class FtpAnta:
	# url = 'cpnits.com'
	# user = 'cpnitswebsite@cpnits.com'
	# password = 'CpnitsWebsite'
	# htmldir = 'public_html'

	def __init__(self, url, user, password, basedir):
		self.url = url
		self.user = user
		self.password = password
		self.basedir = basedir
		try:
			self.anta = FTP(self.url, self.user, self.password)
			self.anta.cwd(self.basedir)
		except:
			pass

	def has_indexhtml(self) -> bool:
		try:
			return 'index.html' in self.anta.nlst()
		except:
			return False

	def get_indexhtml(self) -> any:
		# https://stackoverflow.com/questions/30449269/how-can-i-send-a-stringio-via-ftp-in-python-3
		file = io.BytesIO()
		try:
			with file as fp:
				self.anta.retrbinary(f'RETR index.html', fp.write)
				# file_wrapper = io.TextIOWrapper(file, encoding='utf-8')
				return file.getvalue().decode()
		except:
			return None

	def put_indexhtml(self, html: str) -> bool:
		file = io.BytesIO()
		file_wrapper = io.TextIOWrapper(file, encoding='utf-8')
		file_wrapper.write(html)
		file.seek(0)
		try:
			return bool(self.anta.storbinary(f"STOR index.html", file))
		except:
			return False

	def put_grades(self, jsono: str) -> bool:
		# https://stackoverflow.com/questions/30449269/how-can-i-send-a-stringio-via-ftp-in-python-3
		content_json = bytes(jsono, "utf-8")
		with io.BytesIO(content_json) as fp:
			self.anta.storbinary("STOR grades.json", fp)
		return True
	'''
	def get_file(self, path: str) -> bool:
		try:
			name = path.split('/')[-1]
			return bool(self.anta.storbinary(f"STOR {name}", file))
		except:
			return False
	'''


'''
userspath = os.path.join(Mainroad.get_system_path(), 's_srs.pickle')
userslist = [{'magda': ['docent'], 'alias': 'Iris', 'password': 'trwnvcksghdes'},
 {'magda': ['administratie', 'docent', 'beheer'],
  'alias': 'Jaqueline',
  'password': 'bnuskvbdhyswk'},
 {'magda': ['docent'],
  'alias': 'Sarah',
  'password': 'tgjklncdhsdlobg'},
 {'magda': ['administratie', 'docent', 'beheer', 'admin'],
  'alias': 'Victor',
  'password': 'nr1'},
 {'magda': ['administratie', 'docent', 'beheer'],
  'alias': 'Marcel',
  'password': 'sxtdncdklchnbd'}]

Pickles.write(userspath, userslist)
userslist = Pickles.read(userspath)
ppp(userslist)
'''