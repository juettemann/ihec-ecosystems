#Json hub decription 

A formal definition is at: https://github.com/IHEC/ihec-ecosystems/blob/master/JSON_Data_Hub_Validator/data_hub_schema.json

##Informal description

* A json hub datasets is represented with a hash keyed by experiment identifier.

```
{
    "hub_description": { ... },
    "datasets": { ... }
}
```


* Each dataset experiment key in the hash refers to a hash with following required keys:

```
"datasets": {
    "experiment_1": {
        "sample_attributes": { ... },
        "experiment_attributes": { ... },
        "analysis_attributes": { ... },
        "browser": { ... }
    },
    ...
}
```

* Each of keys 'analysis_attributes', 'experiment_attributes', 'sample_attributes' points to hash containing attributes specified by IHEC Metadata Working group at https://docs.google.com/document/d/1F8RUNGtKMr2lBqMc6pvSyAlZmmtwZxMB3I3u7f7xIbg , with required attributes defined in https://github.com/IHEC/ihec-ecosystems/blob/master/docs/trackhub_specification.md

* 'analysis_group' is a string identifier for the centre processing the data referenced from the hub. 

* 'experiment' is the experiment type. It must be one of the experiment types defined in the Metadata Standards document.


###Tracks:

* The 'browser' key points to a hash of each data track for the experiment. This hash is keyed by a description for the track (the 'type'). Any key is supported, however, only keys corresponding to required track types as defined in https://github.com/IHEC/ihec-ecosystems/blob/master/minimum_required_track_types.md are read. 

* For each 'track type' key under 'browser', the following properties can be provided:
	  * 'big_data_url' : the actual data url
      * 'description_url' *(optional)*: a url with description of methods used to generate the track

* If a track is stranded (forward or reverse), the opposite strand track also needs to be provided.

* For one experiment, a track should be unique for a type/strand combination. (e.g. not having two peak files, or two coverage tracks on the forward strand)

```
"browser": {
	"signal_forward": {
		"big_data_url": "http://mybigWigUrl/mytrack1.bigWig",
		"description_url": "..."
	},
	"signal_reverse": {
		"big_data_url": "http://mybigWigUrl/mytrack2.bigWig",
	}
}
```


###Notes:

* Note that the the format is extensible. You can annotate your data, and include data way beyond the specification.   

* For complete examples (possibly not up to date with latest developments on the spec) see: https://github.com/IHEC/ihec-ecosystems/tree/master/BCGSC_CEMT/Templater/examples and https://github.com/IHEC/ihec-ecosystems/blob/master/JSON_Data_Hub_Validator/example1.json

* Here's a short example: