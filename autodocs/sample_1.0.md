

## Cell Line 

The metadata specification for Cell Line samples is as defined below.

<strong>BATCH</strong>:_undef_.

<strong>DIFFERENTIATION_METHOD</strong>:_undef_.

<strong>DIFFERENTIATION_STAGE</strong>:_undef_.  This attribute is <strong>required</strong>.

<strong>LINE</strong>:_undef_.  This attribute is <strong>required</strong>.

<strong>LINEAGE</strong>:_undef_.  This attribute is <strong>required</strong>.

<strong>MEDIUM</strong>:_undef_.  This attribute is <strong>required</strong>.

<strong>PASSAGE</strong>:_undef_.

<strong>SEX</strong>:_undef_.  This attribute is <strong>required</strong>.


## Primary Cell 

The metadata specification for Primary Cell samples is as defined below.

Additionally, the metadata must also satify requirements for following specifications: <strong>donor</strong>

<strong>CELL_TYPE</strong>:_undef_.  This attribute is <strong>required</strong>.

<strong>MARKERS</strong>:_undef_.

<strong>ORIGIN_SAMPLE</strong>:_undef_.

<strong>ORIGIN_SAMPLE_ONTOLOGY_URI</strong>:(Ontology: UBERON) links to the tissue from which sample was extracted.

<strong>PASSAGE_IF_EXPANDED</strong>:_undef_.


## Primary Cell Culture 

The metadata specification for Primary Cell Culture samples is as defined below.

Additionally, the metadata must also satify requirements for following specifications: <strong>donor</strong>

<strong>CELL_TYPE</strong>:_undef_.  This attribute is <strong>required</strong>.

<strong>CULTURE_CONDITIONS</strong>:_undef_.  This attribute is <strong>required</strong>.

<strong>MARKERS</strong>:_undef_.

<strong>ORIGIN_SAMPLE</strong>:_undef_.

<strong>ORIGIN_SAMPLE_ONTOLOGY_URI</strong>:(Ontology: UBERON) links to the tissue from which sample was extracted.

<strong>PASSAGE_IF_EXPANDED</strong>:_undef_.


## Primary Tissue 

The metadata specification for Primary Tissue samples is as defined below.

Additionally, the metadata must also satify requirements for following specifications: <strong>donor</strong>

<strong>COLLECTION_METHOD</strong>:_undef_.

<strong>TISSUE_DEPOT</strong>:_undef_.  This attribute is <strong>required</strong>.

<strong>TISSUE_TYPE</strong>:_undef_.  This attribute is <strong>required</strong>.


## donor 

The metadata specification for donor samples is as defined below.

<strong>DONOR_AGE</strong>:_undef_.  This attribute is <strong>required</strong>.

<strong>DONOR_AGE_UNIT</strong>:_undef_.  This attribute is <strong>required</strong>.

<strong>DONOR_ETHNICITY</strong>:_undef_.  This attribute is <strong>required</strong>.

<strong>DONOR_HEALTH_STATUS</strong>:_undef_.  This attribute is <strong>required</strong>.

<strong>DONOR_HEALTH_STATUS_ONTOLOGY_URI</strong>:(Ontology: NCIM) Links to the health status of the donor that provided the primary cell. The NCImetathesaurus term C0277545 'Disease type AND/OR category unknown' should be used for unknown diseases. For samples without any known disease, use the NCImetathesaurus term C0549184 'None'. Phenotypes associated with the disease should be submitted as DISEASE_ONTOLOGY_CURIEs (if available) or in the free form DISEASE attribute. If dealing with a rare disease, please consider identifiability issues.

<strong>DONOR_ID</strong>:_undef_.  This attribute is <strong>required</strong>.

<strong>DONOR_LIFE_STAGE</strong>:_undef_.

<strong>DONOR_SEX</strong>:_undef_.  This attribute is <strong>required</strong>.

