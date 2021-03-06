from .utils import json2, cmn, logger
import jsonschema
import os
import string
import json
import sys
import random
from .prevalidate import Prevalidate
from . import egautils

# scrap trying to use ihec_data_hub verbose_error :(
#from pathlib import Path
#sys.path.append(Path(os.path.abspath(Path(__file__).parent)).parent)
#import IHEC_Data_Hub as ihec_data_hub



from .utils import json2

def verbose_error(schema, obj, tag):
	error_log = list()
	v = jsonschema.Draft7Validator(schema)
	errors = [e for e in v.iter_errors(obj)]
	error_log.append('__total_errors__:{}'.format(len(errors)))
    
	for error in sorted(errors, key=str):
		error_log.append('#__validation_error_in__: {2} \n\n# {0}: {1}'.format('.'.join(str(v) for v in error.path), error.message, tag))
		if len(error.context) > 0:
			#error_log.append('Multiple sub-schemas can apply. This is the errors for each:')
			prev_schema = -1
			for suberror in sorted(error.context, key=lambda e: e.schema_path):
				schema_index = suberror.schema_path[0]
				if prev_schema < schema_index:
					error_log.append('__schema_id__:{}'.format(schema_index + 1))
					prev_schema = schema_index
				error_log.append('\t{}'.format(suberror.message))
		error_log.append("--------------------------------------------------")
	return error_log





class Sanitizer:
	def __init__(self):
		pass
	def filter_alphan(self, t, additional):
		return ''.join(filter(lambda x: x.lower() in string.ascii_lowercase or x in additional, t))
	


class JsonSchema:
	def fixfilebase(self, f):
		assert f.startswith(self.expectedpath), [f, self.expectedpath]
		f = self.newpath + f[len(self.expectedpath):]
		schemafile = f.split(':')[-1].split('#')[0]
		if not cmn.fexists(schemafile):
			 logger('#err ...schema file {0} not found\n'.format(schemafile))
		return f

	def obj_id(self, e):
		return egautils.obj_id(e)



	def __init__(self, schema_file, config, version, tag = None, verbose = True, draft4schema=False):
		self.version = version
		self.sanitizer = Sanitizer()
		if not tag:
			tag = cmn.basename(schema_file).split('.')[0]
		self.tag = tag
		self.errdir = '.'
		#if not config.has('-dbg'):
		#	try: os.mkdir("./errlog")
		#	except: pass
		#	self.errdir = "./errlog"
		self.f = schema_file
		self.errs = list()
		self.now  = cmn.now()
		self.verbose = verbose
		self.schema = json2.loadf(self.f)
		self.base = os.path.dirname(os.path.abspath(__file__))
		self.cwd = os.getcwd()
		self.expectedpath = 'file:./schemas/json/' 
		self.newpath = 'file:{0}/schemas/json/'.format(self.cwd, version)
		#self.newpath = 'file:{0}/../schemas/json/{1}'.format(self.base, version)
		if draft4schema:
			raise Exception("__no_longer_supported__")
			for e in self.schema.get('anyOf', list()):
				if '$ref' in e:
					e['$ref'] = self.fixfilebase(e['$ref'])

			for x in self.schema.get('allOf', dict()):
				for e in x['anyOf']:
					if '$ref' in e:
						e['$ref'] = self.fixfilebase(e['$ref'])
		else:
			schema_json = cmn.fread(self.f)
			schema_json_fixed = schema_json.replace(self.expectedpath, self.newpath)
			self.schema = json.loads(schema_json_fixed) 
		print('#__initialized: {0} {1}\n#__path: {2}'.format(self.f, self.version, self.newpath))	
		self.prevalidation = Prevalidate([ json2.copyobj(self.schema)   ],   version) 

	def errlog(self, i, tag):
		#print('xxxxxxxxxxxxxxxxxx', tag)
		if not tag:
			f = '{3}/errs.{2}.{0}.{1}.log'.format(i, self.now, self.tag, self.errdir)
		else:
			f = '{4}/errs.{3}.{0}.{1}.{2}.log'.format(i, tag, self.now, self.tag, self.errdir)
		if not cmn.fexists(f): return f
		for i in range(1000):
			g = f + '.' + ''.join(random.choice(string.ascii_lowercase) for i in range(10)) + '.log'
			if not cmn.fexists(g):
				return g
		raise Exception('__cannot_file_nonexistent_file_starting_with:' +  f)
				
		

	def validate(self, jsonObj, details, schema_version):
		tag = self.obj_id(details)
		prevalidate, errors =  self.prevalidation.prevalidate(jsonObj, tag)
		if prevalidate:
			print('#__prevalidation_passed__', tag, schema_version)
			ok, status =  self.validate_draft7logging(jsonObj, details, schema_version)
		else:
			print('#__prevalidation_failed__', tag, schema_version, '__validation_skipped__')
			ok = False 
			status = {tag : {'error_type' : '__prevalidation__', 'errors' : errors, 'version' : schema_version}}
		#status[tag]['ok'] = ok
		return ok, status
				


		#return self.validate_defaultlogging(jsonObj, details)

	def validate_draft7logging(self, jsonObj, details, schema_version):
		try:
			#logger.entry('#__errors__')
			jsonschema.Draft7Validator(self.schema).validate(jsonObj)
			jsonschema.validate(jsonObj, self.schema, format_checker=jsonschema.FormatChecker())
			#json2.pp(jsonObj)
		
			tag = self.obj_id(details)
			return True, {tag: {'errors' : [], 'ok' : True, 'version' : schema_version}   }
		except jsonschema.ValidationError as err:
			tag = self.obj_id(details)
			#json2.pp(self.schema)
			errors = verbose_error(self.schema, jsonObj, tag) 
			logfile = self.errlog(len(self.errs),  tag + '.ihec_' + schema_version) # self.obj_id(details))
			logger.entry('#__writing_errors[for IHEC spec={1}]: {0}'.format(logfile, schema_version))
			log = []
			with open(logfile, "w") as errfile:
				for e in errors:
					errfile.write(e)
					errfile.write('\n')
					log.append(e)
			return False, {tag : {'errors' :  logfile, 'error_type' : 'jsonschema',  'ok' : False, 'version': schema_version}}
			
				






