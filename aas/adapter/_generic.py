"""
Dicts to serialize enum classes
"""
from typing import Dict

from aas import model

MODELING_KIND: Dict[model.ModelingKind, str] = {
    model.ModelingKind.TEMPLATE: 'Template',
    model.ModelingKind.INSTANCE: 'Instance'}

ASSET_KIND: Dict[model.AssetKind, str] = {
    model.AssetKind.TYPE: 'Type',
    model.AssetKind.INSTANCE: 'Instance'}

KEY_ELEMENTS: Dict[model.KeyElements, str] = {
    model.KeyElements.ASSET: 'Asset',
    model.KeyElements.ASSET_ADMINISTRATION_SHELL: 'AssetAdministrationShell',
    model.KeyElements.CONCEPT_DESCRIPTION: 'ConceptDescription',
    model.KeyElements.SUBMODEL: 'Submodel',
    model.KeyElements.ANNOTATED_RELATIONSHIP_ELEMENT: 'AnnotatedRelationshipElement',
    model.KeyElements.BASIC_EVENT: 'BasicEvent',
    model.KeyElements.BLOB: 'Blob',
    model.KeyElements.CAPABILITY: 'Capability',
    model.KeyElements.CONCEPT_DICTIONARY: 'ConceptDictionary',
    model.KeyElements.DATA_ELEMENT: 'DataElement',
    model.KeyElements.ENTITY: 'Entity',
    model.KeyElements.EVENT: 'Event',
    model.KeyElements.FILE: 'File',
    model.KeyElements.MULTI_LANGUAGE_PROPERTY: 'MultiLanguageProperty',
    model.KeyElements.OPERATION: 'Operation',
    model.KeyElements.PROPERTY: 'Property',
    model.KeyElements.RANGE: 'Range',
    model.KeyElements.REFERENCE_ELEMENT: 'ReferenceElement',
    model.KeyElements.RELATIONSHIP_ELEMENT: 'RelationshipElement',
    model.KeyElements.SUBMODEL_ELEMENT: 'SubmodelElement',
    model.KeyElements.SUBMODEL_ELEMENT_COLLECTION: 'SubmodelElementCollection',
    model.KeyElements.VIEW: 'View',
    model.KeyElements.GLOBAL_REFERENCE: 'GlobalReference',
    model.KeyElements.FRAGMENT_REFERENCE: 'FragmentReference'}

KEY_TYPES: Dict[model.KeyType, str] = {
    model.KeyType.CUSTOM: 'Custom',
    model.KeyType.IRDI: 'IRDI',
    model.KeyType.IRI: 'IRI',
    model.KeyType.IDSHORT: 'IdShort',
    model.KeyType.FRAGMENT_ID: 'FragmentId'}

IDENTIFIER_TYPES: Dict[model.IdentifierType, str] = {
    model.IdentifierType.CUSTOM: 'Custom',
    model.IdentifierType.IRDI: 'IRDI',
    model.IdentifierType.IRI: 'IRI'}

ENTITY_TYPES: Dict[model.EntityType, str] = {
    model.EntityType.CO_MANAGED_ENTITY: 'CoManagedEntity',
    model.EntityType.SELF_MANAGED_ENTITY: 'SelfManagedEntity'}

IEC61360_DATA_TYPES: Dict[model.concept.IEC61360DataType, str] = {
    model.concept.IEC61360DataType.DATE: 'DATE',
    model.concept.IEC61360DataType.STRING: 'STRING',
    model.concept.IEC61360DataType.STRING_TRANSLATABLE: 'STRING_TRANSLATABLE',
    model.concept.IEC61360DataType.REAL_MEASURE: 'REAL_MEASURE',
    model.concept.IEC61360DataType.REAL_COUNT: 'REAL_COUNT',
    model.concept.IEC61360DataType.REAL_CURRENCY: 'REAL_CURRENCY',
    model.concept.IEC61360DataType.BOOLEAN: 'BOOLEAN',
    model.concept.IEC61360DataType.URL: 'URL',
    model.concept.IEC61360DataType.RATIONAL: 'RATIONAL',
    model.concept.IEC61360DataType.RATIONAL_MEASURE: 'RATIONAL_MEASURE',
    model.concept.IEC61360DataType.TIME: 'TIME',
    model.concept.IEC61360DataType.TIMESTAMP: 'TIMESTAMP',
}

IEC61360_LEVEL_TYPES: Dict[model.concept.IEC61360LevelType, str] = {
    model.concept.IEC61360LevelType.MIN: 'Min',
    model.concept.IEC61360LevelType.MAX: 'Max',
    model.concept.IEC61360LevelType.NOM: 'Nom',
    model.concept.IEC61360LevelType.TYP: 'Typ',
}