from .sraparse import SRAParseObjSet, SRAParseObj,  XMLValidator
from .utils import cmn, json2, logger
from .validate_json import JsonSchema
from .ihec_validator_base import  IHECJsonValidator



class SampleValidator(IHECJsonValidator):
	def normalize_tags(self, hashed):
		fix_tag_names =  { self.normalize(k) :v for k, v in hashed.items()}	
		if 'donor_age' in fix_tag_names:
			try:
				fix_tag_names['donor_age'] = [int(val) for val in fix_tag_names['donor_age']]
			except Exception as err:
				logger.warn( '#__warning: failed to cast donor age to number\n'.format(err) + str(fix_tag_names))
		return fix_tag_names 

	def __init__(self, sra, validators):
		super(SampleValidator, self).__init__(validators)
		self.normalize = lambda t: t.lower().replace(' ', '_')
		self.sra = sra
		self.xmljson = self.sra.obj_xmljson()
		for (xml, attrs) in self.xmljson:
			logger(u'\n#__normalizingTags:{0}\n'.format(attrs['title']))
			attrs['attributes'] = self.normalize_tags(attrs['attributes'])
		logger("\n\n")

	def validate_semantics(self, attrs):
		attributes = attrs['attributes']
		if 'donor_age_unit' in attributes and attributes['donor_age_unit'] == 'year' and isinstance(attributes['donor_age'], int):
			age = int(attributes['donor_age'])
			if age > 90:
				logger('#__error: Donors over 90 years of age should be entered as "90+"\n')
				return False

		return True



def main(args):
	print (args['-config'])
	outfile = args['-out']
	config = json2.loadf(args['-config'])
	xml_validator = XMLValidator(config["sra"]["sample"])
	ihec_validators = cmn.safedict([(schema["version"] ,  JsonSchema(schema["schema"], args, version=schema["version"])) for schema in config["ihec"]["sample"]])
	
	objtype = 'SAMPLE'
	objset = 'SAMPLE_SET'

	validated = list()
	xmllist = args.args()
	nObjs = 0
	for e in xmllist:
		sra = SRAParseObjSet.from_file(e)
		nObjs += sra.nOffspring()
		assert  sra.xml.getroot().tag  == objset, ['__Expected:' + objset]
		assert sra.is_valid__xml(xml_validator) or args.has('-not-sra-xml-but-try')
		v = SampleValidator(sra, ihec_validators)
		validated.extend(v.is_valid_ihec())

	versioned_xml = ['<{0}>'.format(objset) ]
	for e in validated:
		(version, xml, tag) = e
		sra_versioned = SRAParseObj(xml)
		sra_versioned.add_attribute("VALIDATED_AGAINST_METADATA_SPEC", "{0}/{1}".format(version, objtype))
		versioned_xml.append(sra_versioned.tostring())
	versioned_xml.append('</{0}>'.format(objset))


	validated_xml_file = cmn.writel(outfile, versioned_xml)
	print ('written:' + validated_xml_file)
	print ('validated:', len(validated))
	print ('failed:', nObjs - len(validated))
	
	if validated:
		validated_xml_set = SRAParseObjSet.from_file(validated_xml_file)
		assert validated_xml_set.is_valid__xml(xml_validator)  or args.has("-skip-updated-xml-validation")
		logger('ok\n')
	else:
		logger('..no valid objects found\n')

	json2.pp({"valid" : [tag + ' = ' + version  for (version, xml, tag) in validated ]})


	





