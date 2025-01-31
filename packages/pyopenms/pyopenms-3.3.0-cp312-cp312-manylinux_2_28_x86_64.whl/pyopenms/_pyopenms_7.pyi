from __future__ import annotations
from typing import overload, Any, List, Dict, Tuple, Set, Sequence, Union
from pyopenms import *  # pylint: disable=wildcard-import; lgtm(py/polluting-import)
import numpy as _np

from enum import Enum as _PyEnum


def __static_VersionDetails_create(in_0: Union[bytes, str, String] ) -> VersionDetails:
    """
    Cython signature: VersionDetails create(String)
    """
    ...

def __static_VersionInfo_getBranch() -> Union[bytes, str, String]:
    """
    Cython signature: String getBranch()
    """
    ...

def __static_TransformationModelBSpline_getDefaultParameters(params: Param ) -> None:
    """
    Cython signature: void getDefaultParameters(Param & params)
    """
    ...

def __static_TransformationModelLowess_getDefaultParameters(params: Param ) -> None:
    """
    Cython signature: void getDefaultParameters(Param & params)
    """
    ...

def __static_VersionInfo_getRevision() -> Union[bytes, str, String]:
    """
    Cython signature: String getRevision()
    """
    ...

def __static_VersionInfo_getTime() -> Union[bytes, str, String]:
    """
    Cython signature: String getTime()
    """
    ...

def __static_VersionInfo_getVersion() -> Union[bytes, str, String]:
    """
    Cython signature: String getVersion()
    """
    ...

def __static_VersionInfo_getVersionStruct() -> VersionDetails:
    """
    Cython signature: VersionDetails getVersionStruct()
    """
    ...

def __static_ChromatogramExtractor_prepare_coordinates(output_chromatograms: List[OSChromatogram] , extraction_coordinates: List[ExtractionCoordinates] , targeted: TargetedExperiment , rt_extraction_window: float , ms1: bool , ms1_isotopes: int ) -> None:
    """
    Cython signature: void prepare_coordinates(libcpp_vector[shared_ptr[OSChromatogram]] & output_chromatograms, libcpp_vector[ExtractionCoordinates] & extraction_coordinates, TargetedExperiment & targeted, double rt_extraction_window, bool ms1, int ms1_isotopes)
    """
    ...


class BiGaussModel:
    """
    Cython implementation of _BiGaussModel

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1BiGaussModel.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void BiGaussModel()
        """
        ...
    
    @overload
    def __init__(self, in_0: BiGaussModel ) -> None:
        """
        Cython signature: void BiGaussModel(BiGaussModel &)
        """
        ...
    
    def setOffset(self, offset: float ) -> None:
        """
        Cython signature: void setOffset(double offset)
        """
        ...
    
    def setSamples(self) -> None:
        """
        Cython signature: void setSamples()
        """
        ...
    
    def getCenter(self) -> float:
        """
        Cython signature: double getCenter()
        """
        ... 


class CVMappingTerm:
    """
    Cython implementation of _CVMappingTerm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVMappingTerm.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVMappingTerm()
        """
        ...
    
    @overload
    def __init__(self, in_0: CVMappingTerm ) -> None:
        """
        Cython signature: void CVMappingTerm(CVMappingTerm &)
        """
        ...
    
    def setAccession(self, accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setAccession(String accession)
        Sets the accession string of the term
        """
        ...
    
    def getAccession(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getAccession()
        Returns the accession string of the term
        """
        ...
    
    def setUseTermName(self, use_term_name: bool ) -> None:
        """
        Cython signature: void setUseTermName(bool use_term_name)
        Sets whether the term name should be used, instead of the accession
        """
        ...
    
    def getUseTermName(self) -> bool:
        """
        Cython signature: bool getUseTermName()
        Returns whether the term name should be used, instead of the accession
        """
        ...
    
    def setUseTerm(self, use_term: bool ) -> None:
        """
        Cython signature: void setUseTerm(bool use_term)
        Sets whether the term itself can be used (or only its children)
        """
        ...
    
    def getUseTerm(self) -> bool:
        """
        Cython signature: bool getUseTerm()
        Returns true if the term can be used, false if only children are allowed
        """
        ...
    
    def setTermName(self, term_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTermName(String term_name)
        Sets the name of the term
        """
        ...
    
    def getTermName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTermName()
        Returns the name of the term
        """
        ...
    
    def setIsRepeatable(self, is_repeatable: bool ) -> None:
        """
        Cython signature: void setIsRepeatable(bool is_repeatable)
        Sets whether this term can be repeated
        """
        ...
    
    def getIsRepeatable(self) -> bool:
        """
        Cython signature: bool getIsRepeatable()
        Returns true if this term can be repeated, false otherwise
        """
        ...
    
    def setAllowChildren(self, allow_children: bool ) -> None:
        """
        Cython signature: void setAllowChildren(bool allow_children)
        Sets whether children of this term are allowed
        """
        ...
    
    def getAllowChildren(self) -> bool:
        """
        Cython signature: bool getAllowChildren()
        Returns true if the children of this term are allowed to be used
        """
        ...
    
    def setCVIdentifierRef(self, cv_identifier_ref: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCVIdentifierRef(String cv_identifier_ref)
        Sets the CV identifier reference string, e.g. UO for unit obo
        """
        ...
    
    def getCVIdentifierRef(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCVIdentifierRef()
        Returns the CV identifier reference string
        """
        ...
    
    def __richcmp__(self, other: CVMappingTerm, op: int) -> Any:
        ... 


class CVTerm:
    """
    Cython implementation of _CVTerm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVTerm.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVTerm()
        """
        ...
    
    @overload
    def __init__(self, in_0: CVTerm ) -> None:
        """
        Cython signature: void CVTerm(CVTerm &)
        """
        ...
    
    def setAccession(self, accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setAccession(String accession)
        Sets the accession string of the term
        """
        ...
    
    def getAccession(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getAccession()
        Returns the accession string of the term
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the name of the term
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the term
        """
        ...
    
    def setCVIdentifierRef(self, cv_id_ref: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCVIdentifierRef(String cv_id_ref)
        Sets the CV identifier reference string, e.g. UO for unit obo
        """
        ...
    
    def getCVIdentifierRef(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCVIdentifierRef()
        Returns the CV identifier reference string
        """
        ...
    
    def getValue(self) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getValue()
        Returns the value of the term
        """
        ...
    
    def setValue(self, value: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setValue(DataValue value)
        Sets the value of the term
        """
        ...
    
    def setUnit(self, unit: Unit ) -> None:
        """
        Cython signature: void setUnit(Unit & unit)
        Sets the unit of the term
        """
        ...
    
    def getUnit(self) -> Unit:
        """
        Cython signature: Unit getUnit()
        Returns the unit
        """
        ...
    
    def hasValue(self) -> bool:
        """
        Cython signature: bool hasValue()
        Checks whether the term has a value
        """
        ...
    
    def hasUnit(self) -> bool:
        """
        Cython signature: bool hasUnit()
        Checks whether the term has a unit
        """
        ...
    
    def __richcmp__(self, other: CVTerm, op: int) -> Any:
        ... 


class ChromatogramExtractor:
    """
    Cython implementation of _ChromatogramExtractor

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ChromatogramExtractor.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ChromatogramExtractor()
        """
        ...
    
    @overload
    def __init__(self, in_0: ChromatogramExtractor ) -> None:
        """
        Cython signature: void ChromatogramExtractor(ChromatogramExtractor &)
        """
        ...
    
    def extractChromatograms(self, input: SpectrumAccessOpenMS , output: List[OSChromatogram] , extraction_coordinates: List[ExtractionCoordinates] , mz_extraction_window: float , ppm: bool , im_extraction_window: float , filter: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void extractChromatograms(shared_ptr[SpectrumAccessOpenMS] input, libcpp_vector[shared_ptr[OSChromatogram]] & output, libcpp_vector[ExtractionCoordinates] extraction_coordinates, double mz_extraction_window, bool ppm, double im_extraction_window, String filter)
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ...
    
    prepare_coordinates: __static_ChromatogramExtractor_prepare_coordinates 


class ChromatogramPeak:
    """
    Cython implementation of _ChromatogramPeak

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ChromatogramPeak_1_1ChromatogramPeak.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ChromatogramPeak()
        A 1-dimensional raw data point or peak for chromatograms
        """
        ...
    
    @overload
    def __init__(self, in_0: ChromatogramPeak ) -> None:
        """
        Cython signature: void ChromatogramPeak(ChromatogramPeak &)
        """
        ...
    
    @overload
    def __init__(self, retention_time: DPosition1 , intensity: float ) -> None:
        """
        Cython signature: void ChromatogramPeak(DPosition1 retention_time, double intensity)
        """
        ...
    
    def getIntensity(self) -> float:
        """
        Cython signature: double getIntensity()
        Returns the intensity
        """
        ...
    
    def setIntensity(self, in_0: float ) -> None:
        """
        Cython signature: void setIntensity(double)
        Sets the intensity
        """
        ...
    
    def getPosition(self) -> DPosition1:
        """
        Cython signature: DPosition1 getPosition()
        """
        ...
    
    def setPosition(self, in_0: DPosition1 ) -> None:
        """
        Cython signature: void setPosition(DPosition1)
        """
        ...
    
    def getRT(self) -> float:
        """
        Cython signature: double getRT()
        Returns the retention time
        """
        ...
    
    def setRT(self, in_0: float ) -> None:
        """
        Cython signature: void setRT(double)
        Sets retention time
        """
        ...
    
    def getPos(self) -> float:
        """
        Cython signature: double getPos()
        Alias for getRT()
        """
        ...
    
    def setPos(self, in_0: float ) -> None:
        """
        Cython signature: void setPos(double)
        Alias for setRT()
        """
        ...
    
    def __richcmp__(self, other: ChromatogramPeak, op: int) -> Any:
        ... 


class ConsensusFeature:
    """
    Cython implementation of _ConsensusFeature

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusFeature.html>`_
      -- Inherits from ['UniqueIdInterface', 'BaseFeature']

    A consensus feature spanning multiple LC-MS/MS experiments.
    
    A ConsensusFeature represents analytes that have been
    quantified across multiple LC-MS/MS experiments. Each analyte in a
    ConsensusFeature is linked to its original LC-MS/MS run through a
    unique identifier.
    
    Get access to the underlying features through getFeatureList()
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ConsensusFeature()
        """
        ...
    
    @overload
    def __init__(self, in_0: ConsensusFeature ) -> None:
        """
        Cython signature: void ConsensusFeature(ConsensusFeature &)
        """
        ...
    
    @overload
    def __init__(self, in_0: int , in_1: Peak2D , in_2: int ) -> None:
        """
        Cython signature: void ConsensusFeature(uint64_t, Peak2D, uint64_t)
        """
        ...
    
    @overload
    def __init__(self, in_0: int , in_1: BaseFeature ) -> None:
        """
        Cython signature: void ConsensusFeature(uint64_t, BaseFeature)
        """
        ...
    
    @overload
    def __init__(self, in_0: int , in_1: ConsensusFeature ) -> None:
        """
        Cython signature: void ConsensusFeature(uint64_t, ConsensusFeature)
        """
        ...
    
    def computeConsensus(self) -> None:
        """
        Cython signature: void computeConsensus()
        Computes and updates the consensus position, intensity, and charge
        """
        ...
    
    def computeMonoisotopicConsensus(self) -> None:
        """
        Cython signature: void computeMonoisotopicConsensus()
        Computes and updates the consensus position, intensity, and charge
        """
        ...
    
    def computeDechargeConsensus(self, in_0: FeatureMap , in_1: bool ) -> None:
        """
        Cython signature: void computeDechargeConsensus(FeatureMap, bool)
        Computes the uncharged parent RT & mass, assuming the handles are charge variants
        """
        ...
    
    @overload
    def insert(self, map_idx: int , in_1: Peak2D , element_idx: int ) -> None:
        """
        Cython signature: void insert(uint64_t map_idx, Peak2D, uint64_t element_idx)
        """
        ...
    
    @overload
    def insert(self, map_idx: int , in_1: BaseFeature ) -> None:
        """
        Cython signature: void insert(uint64_t map_idx, BaseFeature)
        """
        ...
    
    @overload
    def insert(self, map_idx: int , in_1: ConsensusFeature ) -> None:
        """
        Cython signature: void insert(uint64_t map_idx, ConsensusFeature)
        """
        ...
    
    def getFeatureList(self) -> List[FeatureHandle]:
        """
        Cython signature: libcpp_vector[FeatureHandle] getFeatureList()
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ...
    
    def addRatio(self, r: Ratio ) -> None:
        """
        Cython signature: void addRatio(Ratio r)
        Connects a ratio to the ConsensusFeature.
        """
        ...
    
    def setRatios(self, rs: List[Ratio] ) -> None:
        """
        Cython signature: void setRatios(libcpp_vector[Ratio] rs)
        Connects the ratios to the ConsensusFeature.
        """
        ...
    
    def getRatios(self) -> List[Ratio]:
        """
        Cython signature: libcpp_vector[Ratio] getRatios()
        Get the ratio vector.
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        """
        ...
    
    def getUniqueId(self) -> int:
        """
        Cython signature: size_t getUniqueId()
        Returns the unique id
        """
        ...
    
    def clearUniqueId(self) -> int:
        """
        Cython signature: size_t clearUniqueId()
        Clear the unique id. The new unique id will be invalid. Returns 1 if the unique id was changed, 0 otherwise
        """
        ...
    
    def hasValidUniqueId(self) -> int:
        """
        Cython signature: size_t hasValidUniqueId()
        Returns whether the unique id is valid. Returns 1 if the unique id is valid, 0 otherwise
        """
        ...
    
    def hasInvalidUniqueId(self) -> int:
        """
        Cython signature: size_t hasInvalidUniqueId()
        Returns whether the unique id is invalid. Returns 1 if the unique id is invalid, 0 otherwise
        """
        ...
    
    def setUniqueId(self, rhs: int ) -> None:
        """
        Cython signature: void setUniqueId(uint64_t rhs)
        Assigns a new, valid unique id. Always returns 1
        """
        ...
    
    def ensureUniqueId(self) -> int:
        """
        Cython signature: size_t ensureUniqueId()
        Assigns a valid unique id, but only if the present one is invalid. Returns 1 if the unique id was changed, 0 otherwise
        """
        ...
    
    def isValid(self, unique_id: int ) -> bool:
        """
        Cython signature: bool isValid(uint64_t unique_id)
        Returns true if the unique_id is valid, false otherwise
        """
        ...
    
    def getQuality(self) -> float:
        """
        Cython signature: float getQuality()
        Returns the overall quality
        """
        ...
    
    def setQuality(self, q: float ) -> None:
        """
        Cython signature: void setQuality(float q)
        Sets the overall quality
        """
        ...
    
    def getWidth(self) -> float:
        """
        Cython signature: float getWidth()
        Returns the features width (full width at half max, FWHM)
        """
        ...
    
    def setWidth(self, q: float ) -> None:
        """
        Cython signature: void setWidth(float q)
        Sets the width of the feature (FWHM)
        """
        ...
    
    def getCharge(self) -> int:
        """
        Cython signature: int getCharge()
        Returns the charge state
        """
        ...
    
    def setCharge(self, q: int ) -> None:
        """
        Cython signature: void setCharge(int q)
        Sets the charge state
        """
        ...
    
    def getAnnotationState(self) -> int:
        """
        Cython signature: AnnotationState getAnnotationState()
        State of peptide identifications attached to this feature. If one ID has multiple hits, the output depends on the top-hit only
        """
        ...
    
    def getPeptideIdentifications(self) -> List[PeptideIdentification]:
        """
        Cython signature: libcpp_vector[PeptideIdentification] getPeptideIdentifications()
        Returns the PeptideIdentification vector
        """
        ...
    
    def setPeptideIdentifications(self, peptides: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void setPeptideIdentifications(libcpp_vector[PeptideIdentification] & peptides)
        Sets the PeptideIdentification vector
        """
        ...
    
    def getIntensity(self) -> float:
        """
        Cython signature: float getIntensity()
        Returns the data point intensity (height)
        """
        ...
    
    def getMZ(self) -> float:
        """
        Cython signature: double getMZ()
        Returns the m/z coordinate (index 1)
        """
        ...
    
    def getRT(self) -> float:
        """
        Cython signature: double getRT()
        Returns the RT coordinate (index 0)
        """
        ...
    
    def setMZ(self, in_0: float ) -> None:
        """
        Cython signature: void setMZ(double)
        Returns the m/z coordinate (index 1)
        """
        ...
    
    def setRT(self, in_0: float ) -> None:
        """
        Cython signature: void setRT(double)
        Returns the RT coordinate (index 0)
        """
        ...
    
    def setIntensity(self, in_0: float ) -> None:
        """
        Cython signature: void setIntensity(float)
        Returns the data point intensity (height)
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def __richcmp__(self, other: ConsensusFeature, op: int) -> Any:
        ... 


class ConsensusIDAlgorithmSimilarity:
    """
    Cython implementation of _ConsensusIDAlgorithmSimilarity

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusIDAlgorithmSimilarity.html>`_
      -- Inherits from ['ConsensusIDAlgorithm']
    """
    
    def apply(self, ids: List[PeptideIdentification] , number_of_runs: int ) -> None:
        """
        Cython signature: void apply(libcpp_vector[PeptideIdentification] & ids, size_t number_of_runs)
        Calculates the consensus ID for a set of peptide identifications of one spectrum or (consensus) feature
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class ConsensusMapNormalizerAlgorithmThreshold:
    """
    Cython implementation of _ConsensusMapNormalizerAlgorithmThreshold

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusMapNormalizerAlgorithmThreshold.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusMapNormalizerAlgorithmThreshold()
        """
        ...
    
    def computeCorrelation(self, input_map: ConsensusMap , ratio_threshold: float , acc_filter: Union[bytes, str, String] , desc_filter: Union[bytes, str, String] ) -> List[float]:
        """
        Cython signature: libcpp_vector[double] computeCorrelation(ConsensusMap & input_map, double ratio_threshold, const String & acc_filter, const String & desc_filter)
        Determines the ratio of all maps to the map with the most features
        """
        ...
    
    def normalizeMaps(self, input_map: ConsensusMap , ratios: List[float] ) -> None:
        """
        Cython signature: void normalizeMaps(ConsensusMap & input_map, libcpp_vector[double] & ratios)
        Applies the given ratio to the maps of the consensusMap
        """
        ... 


class CsvFile:
    """
    Cython implementation of _CsvFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CsvFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CsvFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: CsvFile ) -> None:
        """
        Cython signature: void CsvFile(CsvFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , is_: bytes , ie_: bool , first_n: int ) -> None:
        """
        Cython signature: void load(const String & filename, char is_, bool ie_, int first_n)
        Loads data from a text file
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void store(const String & filename)
        Stores the buffer's content into a file
        """
        ...
    
    def addRow(self, list: List[bytes] ) -> None:
        """
        Cython signature: void addRow(const StringList & list)
        Add a row to the buffer
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        Clears the buffer
        """
        ...
    
    def getRow(self, row: int , list: List[bytes] ) -> bool:
        """
        Cython signature: bool getRow(int row, StringList & list)
        Writes all items from a row to list
        """
        ... 


class DistanceMatrix:
    """
    Cython implementation of _DistanceMatrix[float]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DistanceMatrix[float].html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DistanceMatrix()
        """
        ...
    
    @overload
    def __init__(self, in_0: DistanceMatrix ) -> None:
        """
        Cython signature: void DistanceMatrix(DistanceMatrix &)
        """
        ...
    
    @overload
    def __init__(self, dimensionsize: int , value: float ) -> None:
        """
        Cython signature: void DistanceMatrix(size_t dimensionsize, float value)
        """
        ...
    
    def getValue(self, i: int , j: int ) -> float:
        """
        Cython signature: float getValue(size_t i, size_t j)
        """
        ...
    
    def setValue(self, i: int , j: int , value: float ) -> None:
        """
        Cython signature: void setValue(size_t i, size_t j, float value)
        """
        ...
    
    def setValueQuick(self, i: int , j: int , value: float ) -> None:
        """
        Cython signature: void setValueQuick(size_t i, size_t j, float value)
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ...
    
    def resize(self, dimensionsize: int , value: float ) -> None:
        """
        Cython signature: void resize(size_t dimensionsize, float value)
        """
        ...
    
    def reduce(self, j: int ) -> None:
        """
        Cython signature: void reduce(size_t j)
        """
        ...
    
    def dimensionsize(self) -> int:
        """
        Cython signature: size_t dimensionsize()
        """
        ...
    
    def updateMinElement(self) -> None:
        """
        Cython signature: void updateMinElement()
        """
        ...
    
    def getMinElementCoordinates(self) -> List[int, int]:
        """
        Cython signature: libcpp_pair[size_t,size_t] getMinElementCoordinates()
        """
        ...
    
    def __richcmp__(self, other: DistanceMatrix, op: int) -> Any:
        ... 


class Element:
    """
    Cython implementation of _Element

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Element.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Element()
        """
        ...
    
    @overload
    def __init__(self, in_0: Element ) -> None:
        """
        Cython signature: void Element(Element &)
        """
        ...
    
    @overload
    def __init__(self, name: Union[bytes, str, String] , symbol: Union[bytes, str, String] , atomic_number: int , average_weight: float , mono_weight: float , isotopes: IsotopeDistribution ) -> None:
        """
        Cython signature: void Element(String name, String symbol, unsigned int atomic_number, double average_weight, double mono_weight, IsotopeDistribution isotopes)
        """
        ...
    
    def setAtomicNumber(self, atomic_number: int ) -> None:
        """
        Cython signature: void setAtomicNumber(unsigned int atomic_number)
        Sets unique atomic number
        """
        ...
    
    def getAtomicNumber(self) -> int:
        """
        Cython signature: unsigned int getAtomicNumber()
        Returns the unique atomic number
        """
        ...
    
    def setAverageWeight(self, weight: float ) -> None:
        """
        Cython signature: void setAverageWeight(double weight)
        Sets the average weight of the element
        """
        ...
    
    def getAverageWeight(self) -> float:
        """
        Cython signature: double getAverageWeight()
        Returns the average weight of the element
        """
        ...
    
    def setMonoWeight(self, weight: float ) -> None:
        """
        Cython signature: void setMonoWeight(double weight)
        Sets the mono isotopic weight of the element
        """
        ...
    
    def getMonoWeight(self) -> float:
        """
        Cython signature: double getMonoWeight()
        Returns the mono isotopic weight of the element
        """
        ...
    
    def setIsotopeDistribution(self, isotopes: IsotopeDistribution ) -> None:
        """
        Cython signature: void setIsotopeDistribution(IsotopeDistribution isotopes)
        Sets the isotope distribution of the element
        """
        ...
    
    def getIsotopeDistribution(self) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution getIsotopeDistribution()
        Returns the isotope distribution of the element
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the name of the element
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the element
        """
        ...
    
    def setSymbol(self, symbol: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSymbol(String symbol)
        Sets symbol of the element
        """
        ...
    
    def getSymbol(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSymbol()
        Returns symbol of the element
        """
        ... 


class ElementDB:
    """
    Cython implementation of _ElementDB

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ElementDB.html>`_
    """
    
    @overload
    def getElement(self, name: Union[bytes, str, String] ) -> Element:
        """
        Cython signature: const Element * getElement(const String & name)
        """
        ...
    
    @overload
    def getElement(self, atomic_number: int ) -> Element:
        """
        Cython signature: const Element * getElement(unsigned int atomic_number)
        """
        ...
    
    def addElement(self, name: bytes , symbol: bytes , an: int , abundance: Dict[int, float] , mass: Dict[int, float] , replace_existing: bool ) -> None:
        """
        Cython signature: void addElement(libcpp_string name, libcpp_string symbol, unsigned int an, libcpp_map[unsigned int,double] abundance, libcpp_map[unsigned int,double] mass, bool replace_existing)
        """
        ...
    
    @overload
    def hasElement(self, name: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasElement(const String & name)
        Returns true if the db contains an element with the given name, else false
        """
        ...
    
    @overload
    def hasElement(self, atomic_number: int ) -> bool:
        """
        Cython signature: bool hasElement(unsigned int atomic_number)
        Returns true if the db contains an element with the given atomic_number, else false
        """
        ... 


class EmgGradientDescent:
    """
    Cython implementation of _EmgGradientDescent

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1EmgGradientDescent.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void EmgGradientDescent()
        Compute the area, background and shape metrics of a peak
        """
        ...
    
    @overload
    def __init__(self, in_0: EmgGradientDescent ) -> None:
        """
        Cython signature: void EmgGradientDescent(EmgGradientDescent &)
        """
        ...
    
    def getDefaultParameters(self, in_0: Param ) -> None:
        """
        Cython signature: void getDefaultParameters(Param &)
        """
        ...
    
    @overload
    def fitEMGPeakModel(self, input_peak: MSChromatogram , output_peak: MSChromatogram ) -> None:
        """
        Cython signature: void fitEMGPeakModel(MSChromatogram & input_peak, MSChromatogram & output_peak)
        """
        ...
    
    @overload
    def fitEMGPeakModel(self, input_peak: MSSpectrum , output_peak: MSSpectrum ) -> None:
        """
        Cython signature: void fitEMGPeakModel(MSSpectrum & input_peak, MSSpectrum & output_peak)
        """
        ...
    
    @overload
    def fitEMGPeakModel(self, input_peak: MSChromatogram , output_peak: MSChromatogram , left_pos: float , right_pos: float ) -> None:
        """
        Cython signature: void fitEMGPeakModel(MSChromatogram & input_peak, MSChromatogram & output_peak, double left_pos, double right_pos)
        """
        ...
    
    @overload
    def fitEMGPeakModel(self, input_peak: MSSpectrum , output_peak: MSSpectrum , left_pos: float , right_pos: float ) -> None:
        """
        Cython signature: void fitEMGPeakModel(MSSpectrum & input_peak, MSSpectrum & output_peak, double left_pos, double right_pos)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class ExperimentalSettings:
    """
    Cython implementation of _ExperimentalSettings

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ExperimentalSettings.html>`_
      -- Inherits from ['DocumentIdentifier', 'MetaInfoInterface']

    Description of the experimental settings, provides meta-information
    about an LC-MS/MS injection.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ExperimentalSettings()
        """
        ...
    
    @overload
    def __init__(self, in_0: ExperimentalSettings ) -> None:
        """
        Cython signature: void ExperimentalSettings(ExperimentalSettings &)
        """
        ...
    
    def getSourceFiles(self) -> List[SourceFile]:
        """
        Cython signature: libcpp_vector[SourceFile] getSourceFiles()
        Returns a reference to the source data file
        """
        ...
    
    def setSourceFiles(self, source_files: List[SourceFile] ) -> None:
        """
        Cython signature: void setSourceFiles(libcpp_vector[SourceFile] source_files)
        Sets the source data file
        """
        ...
    
    def getDateTime(self) -> DateTime:
        """
        Cython signature: DateTime getDateTime()
        Returns the date the experiment was performed
        """
        ...
    
    def setDateTime(self, date_time: DateTime ) -> None:
        """
        Cython signature: void setDateTime(DateTime date_time)
        Sets the date the experiment was performed
        """
        ...
    
    def getSample(self) -> Sample:
        """
        Cython signature: Sample getSample()
        Returns a reference to the sample description
        """
        ...
    
    def setSample(self, sample: Sample ) -> None:
        """
        Cython signature: void setSample(Sample sample)
        Sets the sample description
        """
        ...
    
    def getContacts(self) -> List[ContactPerson]:
        """
        Cython signature: libcpp_vector[ContactPerson] getContacts()
        Returns a reference to the list of contact persons
        """
        ...
    
    def setContacts(self, contacts: List[ContactPerson] ) -> None:
        """
        Cython signature: void setContacts(libcpp_vector[ContactPerson] contacts)
        Sets the list of contact persons
        """
        ...
    
    def getInstrument(self) -> Instrument:
        """
        Cython signature: Instrument getInstrument()
        Returns a reference to the MS instrument description
        """
        ...
    
    def setInstrument(self, instrument: Instrument ) -> None:
        """
        Cython signature: void setInstrument(Instrument instrument)
        Sets the MS instrument description
        """
        ...
    
    def getHPLC(self) -> HPLC:
        """
        Cython signature: HPLC getHPLC()
        Returns a reference to the description of the HPLC run
        """
        ...
    
    def setHPLC(self, hplc: HPLC ) -> None:
        """
        Cython signature: void setHPLC(HPLC hplc)
        Sets the description of the HPLC run
        """
        ...
    
    def getComment(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getComment()
        Returns the free-text comment
        """
        ...
    
    def setComment(self, comment: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setComment(String comment)
        Sets the free-text comment
        """
        ...
    
    def getProteinIdentifications(self) -> List[ProteinIdentification]:
        """
        Cython signature: libcpp_vector[ProteinIdentification] getProteinIdentifications()
        Returns a reference to the protein ProteinIdentification vector
        """
        ...
    
    def setProteinIdentifications(self, protein_identifications: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void setProteinIdentifications(libcpp_vector[ProteinIdentification] protein_identifications)
        Sets the protein ProteinIdentification vector
        """
        ...
    
    def getFractionIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFractionIdentifier()
        Returns fraction identifier
        """
        ...
    
    def setFractionIdentifier(self, fraction_identifier: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFractionIdentifier(String fraction_identifier)
        Sets the fraction identifier
        """
        ...
    
    def setIdentifier(self, id: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(String id)
        Sets document identifier (e.g. an LSID)
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        Retrieve document identifier (e.g. an LSID)
        """
        ...
    
    def setLoadedFileType(self, file_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setLoadedFileType(String file_name)
        Sets the file_type according to the type of the file loaded from, preferably done whilst loading
        """
        ...
    
    def getLoadedFileType(self) -> int:
        """
        Cython signature: int getLoadedFileType()
        Returns the file_type (e.g. featureXML, consensusXML, mzData, mzXML, mzML, ...) of the file loaded
        """
        ...
    
    def setLoadedFilePath(self, file_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setLoadedFilePath(String file_name)
        Sets the file_name according to absolute path of the file loaded, preferably done whilst loading
        """
        ...
    
    def getLoadedFilePath(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getLoadedFilePath()
        Returns the file_name which is the absolute path to the file loaded
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def __richcmp__(self, other: ExperimentalSettings, op: int) -> Any:
        ... 


class FeatureGroupingAlgorithmLabeled:
    """
    Cython implementation of _FeatureGroupingAlgorithmLabeled

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureGroupingAlgorithmLabeled.html>`_
      -- Inherits from ['FeatureGroupingAlgorithm']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureGroupingAlgorithmLabeled()
        """
        ...
    
    def group(self, maps: List[FeatureMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void group(libcpp_vector[FeatureMap] & maps, ConsensusMap & out)
        """
        ...
    
    def transferSubelements(self, maps: List[ConsensusMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void transferSubelements(libcpp_vector[ConsensusMap] maps, ConsensusMap & out)
        Transfers subelements (grouped features) from input consensus maps to the result consensus map
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class IdXMLFile:
    """
    Cython implementation of _IdXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IdXMLFile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void IdXMLFile()
        Used to load and store idXML files
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , protein_ids: List[ProteinIdentification] , peptide_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void load(String filename, libcpp_vector[ProteinIdentification] & protein_ids, libcpp_vector[PeptideIdentification] & peptide_ids)
        Loads the identifications of an idXML file without identifier
        """
        ...
    
    @overload
    def store(self, filename: Union[bytes, str, String] , protein_ids: List[ProteinIdentification] , peptide_ids: List[PeptideIdentification] , document_id: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void store(String filename, libcpp_vector[ProteinIdentification] & protein_ids, libcpp_vector[PeptideIdentification] & peptide_ids, String document_id)
        Stores the data in an idXML file
        """
        ...
    
    @overload
    def store(self, filename: Union[bytes, str, String] , protein_ids: List[ProteinIdentification] , peptide_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void store(String filename, libcpp_vector[ProteinIdentification] & protein_ids, libcpp_vector[PeptideIdentification] & peptide_ids)
        """
        ... 


class IsobaricIsotopeCorrector:
    """
    Cython implementation of _IsobaricIsotopeCorrector

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsobaricIsotopeCorrector.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IsobaricIsotopeCorrector()
        """
        ...
    
    @overload
    def __init__(self, in_0: IsobaricIsotopeCorrector ) -> None:
        """
        Cython signature: void IsobaricIsotopeCorrector(IsobaricIsotopeCorrector &)
        """
        ...
    
    @overload
    def correctIsotopicImpurities(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap , quant_method: ItraqEightPlexQuantitationMethod ) -> IsobaricQuantifierStatistics:
        """
        Cython signature: IsobaricQuantifierStatistics correctIsotopicImpurities(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out, ItraqEightPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def correctIsotopicImpurities(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap , quant_method: ItraqFourPlexQuantitationMethod ) -> IsobaricQuantifierStatistics:
        """
        Cython signature: IsobaricQuantifierStatistics correctIsotopicImpurities(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out, ItraqFourPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def correctIsotopicImpurities(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap , quant_method: TMTSixPlexQuantitationMethod ) -> IsobaricQuantifierStatistics:
        """
        Cython signature: IsobaricQuantifierStatistics correctIsotopicImpurities(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out, TMTSixPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def correctIsotopicImpurities(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap , quant_method: TMTTenPlexQuantitationMethod ) -> IsobaricQuantifierStatistics:
        """
        Cython signature: IsobaricQuantifierStatistics correctIsotopicImpurities(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out, TMTTenPlexQuantitationMethod * quant_method)
        """
        ... 


class IsotopeFitter1D:
    """
    Cython implementation of _IsotopeFitter1D

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsotopeFitter1D.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IsotopeFitter1D()
        Isotope distribution fitter (1-dim.) approximated using linear interpolation
        """
        ...
    
    @overload
    def __init__(self, in_0: IsotopeFitter1D ) -> None:
        """
        Cython signature: void IsotopeFitter1D(IsotopeFitter1D &)
        """
        ... 


class KDTreeFeatureMaps:
    """
    Cython implementation of _KDTreeFeatureMaps

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1KDTreeFeatureMaps.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void KDTreeFeatureMaps()
        Stores a set of features, together with a 2D tree for fast search
        """
        ...
    
    @overload
    def __init__(self, maps: List[FeatureMap] , param: Param ) -> None:
        """
        Cython signature: void KDTreeFeatureMaps(libcpp_vector[FeatureMap] & maps, Param & param)
        """
        ...
    
    @overload
    def __init__(self, maps: List[ConsensusMap] , param: Param ) -> None:
        """
        Cython signature: void KDTreeFeatureMaps(libcpp_vector[ConsensusMap] & maps, Param & param)
        """
        ...
    
    @overload
    def addMaps(self, maps: List[FeatureMap] ) -> None:
        """
        Cython signature: void addMaps(libcpp_vector[FeatureMap] & maps)
        Add `maps` and balance kd-tree
        """
        ...
    
    @overload
    def addMaps(self, maps: List[ConsensusMap] ) -> None:
        """
        Cython signature: void addMaps(libcpp_vector[ConsensusMap] & maps)
        """
        ...
    
    def rt(self, i: int ) -> float:
        """
        Cython signature: double rt(size_t i)
        """
        ...
    
    def mz(self, i: int ) -> float:
        """
        Cython signature: double mz(size_t i)
        """
        ...
    
    def intensity(self, i: int ) -> float:
        """
        Cython signature: float intensity(size_t i)
        """
        ...
    
    def charge(self, i: int ) -> int:
        """
        Cython signature: int charge(size_t i)
        """
        ...
    
    def mapIndex(self, i: int ) -> int:
        """
        Cython signature: size_t mapIndex(size_t i)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ...
    
    def treeSize(self) -> int:
        """
        Cython signature: size_t treeSize()
        """
        ...
    
    def numMaps(self) -> int:
        """
        Cython signature: size_t numMaps()
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ...
    
    def optimizeTree(self) -> None:
        """
        Cython signature: void optimizeTree()
        """
        ...
    
    def getNeighborhood(self, index: int , result_indices: List[int] , rt_tol: float , mz_tol: float , mz_ppm: bool , include_features_from_same_map: bool , max_pairwise_log_fc: float ) -> None:
        """
        Cython signature: void getNeighborhood(size_t index, libcpp_vector[size_t] & result_indices, double rt_tol, double mz_tol, bool mz_ppm, bool include_features_from_same_map, double max_pairwise_log_fc)
        Fill `result` with indices of all features compatible (wrt. RT, m/z, map index) to the feature with `index`
        """
        ...
    
    def queryRegion(self, rt_low: float , rt_high: float , mz_low: float , mz_high: float , result_indices: List[int] , ignored_map_index: int ) -> None:
        """
        Cython signature: void queryRegion(double rt_low, double rt_high, double mz_low, double mz_high, libcpp_vector[size_t] & result_indices, size_t ignored_map_index)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class KDTreeFeatureNode:
    """
    Cython implementation of _KDTreeFeatureNode

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1KDTreeFeatureNode.html>`_
    """
    
    @overload
    def __init__(self, in_0: KDTreeFeatureNode ) -> None:
        """
        Cython signature: void KDTreeFeatureNode(KDTreeFeatureNode &)
        """
        ...
    
    @overload
    def __init__(self, data: KDTreeFeatureMaps , idx: int ) -> None:
        """
        Cython signature: void KDTreeFeatureNode(KDTreeFeatureMaps * data, size_t idx)
        """
        ...
    
    def __getitem__(self, i: int ) -> float:
        """
        Cython signature: double operator[](size_t i)
        """
        ...
    
    def getIndex(self) -> int:
        """
        Cython signature: size_t getIndex()
        Returns index of corresponding feature in data_
        """
        ... 


class KroenikFile:
    """
    Cython implementation of _KroenikFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1KroenikFile.html>`_

    File adapter for Kroenik (HardKloer sibling) files
    
    The first line is the header and contains the column names:
    File,  First Scan,  Last Scan,  Num of Scans,  Charge,  Monoisotopic Mass,  Base Isotope Peak,  Best Intensity,  Summed Intensity,  First RTime,  Last RTime,  Best RTime,  Best Correlation,  Modifications
    
    Every subsequent line is a feature
    
    All properties in the file are converted to Feature properties, whereas "First Scan", "Last Scan", "Num of Scans" and "Modifications" are stored as
    metavalues with the following names "FirstScan", "LastScan", "NumOfScans" and "AveragineModifications"
    
    The width in m/z of the overall convex hull of each feature is set to 3 Th in lack of a value provided by the Kroenik file
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void KroenikFile()
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void store(String filename, MSSpectrum & spectrum)
        Stores a MSExperiment into a Kroenik file
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , feature_map: FeatureMap ) -> None:
        """
        Cython signature: void load(String filename, FeatureMap & feature_map)
        Loads a Kroenik file into a featureXML
        
        The content of the file is stored in `features`
        
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ... 


class LinearResamplerAlign:
    """
    Cython implementation of _LinearResamplerAlign

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1LinearResamplerAlign.html>`_
      -- Inherits from ['LinearResampler']
    """
    
    def __init__(self, in_0: LinearResamplerAlign ) -> None:
        """
        Cython signature: void LinearResamplerAlign(LinearResamplerAlign &)
        """
        ...
    
    def raster(self, input: MSSpectrum ) -> None:
        """
        Cython signature: void raster(MSSpectrum & input)
        Applies the resampling algorithm to an MSSpectrum
        """
        ...
    
    def rasterExperiment(self, input: MSExperiment ) -> None:
        """
        Cython signature: void rasterExperiment(MSExperiment & input)
        Resamples the data in an MSExperiment
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class MS2File:
    """
    Cython implementation of _MS2File

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MS2File.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MS2File()
        """
        ...
    
    @overload
    def __init__(self, in_0: MS2File ) -> None:
        """
        Cython signature: void MS2File(MS2File &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , exp: MSExperiment ) -> None:
        """
        Cython signature: void load(const String & filename, MSExperiment & exp)
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class MSDataCachedConsumer:
    """
    Cython implementation of _MSDataCachedConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSDataCachedConsumer.html>`_

    Transforming and cached writing consumer of MS data
    
    Is able to transform a spectrum on the fly while it is read using a
    function pointer that can be set on the object. The spectra is then
    cached to disk using the functions provided in CachedMzMLHandler.
    """
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void MSDataCachedConsumer(String filename)
        """
        ...
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] , clear: bool ) -> None:
        """
        Cython signature: void MSDataCachedConsumer(String filename, bool clear)
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        Write a spectrum to the output file
        
        May delete data from spectrum (if clearData is set)
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
        Write a chromatogram to the output file
        
        May delete data from chromatogram (if clearData is set)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings & exp)
        """
        ...
    
    def setExpectedSize(self, expectedSpectra: int , expectedChromatograms: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t expectedSpectra, size_t expectedChromatograms)
        """
        ... 


class MSExperiment:
    """
    Cython implementation of _MSExperiment

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSExperiment.html>`_
      -- Inherits from ['ExperimentalSettings', 'RangeManagerRtMzInt']

    In-Memory representation of a mass spectrometry experiment.
    
    Contains the data and metadata of an experiment performed with an MS (or
    HPLC and MS). This representation of an MS experiment is organized as list
    of spectra and chromatograms and provides an in-memory representation of
    popular mass-spectrometric file formats such as mzXML or mzML. The
    meta-data associated with an experiment is contained in
    ExperimentalSettings (by inheritance) while the raw data (as well as
    spectra and chromatogram level meta data) is stored in objects of type
    MSSpectrum and MSChromatogram, which are accessible through the getSpectrum
    and getChromatogram functions.
    
    Spectra can be accessed by direct iteration or by getSpectrum(),
    while chromatograms are accessed through getChromatogram().
    See help(ExperimentalSettings) for information about meta-data.
    
    Usage:
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MSExperiment()
        """
        ...
    
    @overload
    def __init__(self, in_0: MSExperiment ) -> None:
        """
        Cython signature: void MSExperiment(MSExperiment &)
        """
        ...
    
    def getExperimentalSettings(self) -> ExperimentalSettings:
        """
        Cython signature: ExperimentalSettings getExperimentalSettings()
        """
        ...
    
    def __getitem__(self, in_0: int ) -> MSSpectrum:
        """
        Cython signature: MSSpectrum & operator[](size_t)
        """
        ...
    def __setitem__(self, key: int, value: MSSpectrum ) -> None:
        """Cython signature: MSSpectrum & operator[](size_t)"""
        ...
    
    def addSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void addSpectrum(MSSpectrum spec)
        """
        ...
    
    def setSpectra(self, spectra: List[MSSpectrum] ) -> None:
        """
        Cython signature: void setSpectra(libcpp_vector[MSSpectrum] & spectra)
        """
        ...
    
    def getSpectra(self) -> List[MSSpectrum]:
        """
        Cython signature: libcpp_vector[MSSpectrum] getSpectra()
        """
        ...
    
    def aggregateFromMatrix(self, ranges: MatrixDouble , ms_level: int , mz_agg: bytes ) -> List[List[float]]:
        """
        Cython signature: libcpp_vector[libcpp_vector[double]] aggregateFromMatrix(MatrixDouble & ranges, unsigned int ms_level, libcpp_string mz_agg)
        Aggregates intensity values for multiple m/z and RT ranges specified in a matrix
        """
        ...
    
    def extractXICsFromMatrix(self, ranges: MatrixDouble , ms_level: int , mz_agg: bytes ) -> List[MSChromatogram]:
        """
        Cython signature: libcpp_vector[MSChromatogram] extractXICsFromMatrix(MatrixDouble & ranges, unsigned int ms_level, libcpp_string mz_agg)
        Extracts XIC chromatograms for multiple m/z and RT ranges specified in a matrix
        """
        ...
    
    def addChromatogram(self, chromatogram: MSChromatogram ) -> None:
        """
        Cython signature: void addChromatogram(MSChromatogram chromatogram)
        """
        ...
    
    def setChromatograms(self, chromatograms: List[MSChromatogram] ) -> None:
        """
        Cython signature: void setChromatograms(libcpp_vector[MSChromatogram] chromatograms)
        """
        ...
    
    def getChromatograms(self) -> List[MSChromatogram]:
        """
        Cython signature: libcpp_vector[MSChromatogram] getChromatograms()
        """
        ...
    
    def calculateTIC(self) -> MSChromatogram:
        """
        Cython signature: MSChromatogram calculateTIC()
        Returns the total ion chromatogram
        """
        ...
    
    def clear(self, clear_meta_data: bool ) -> None:
        """
        Cython signature: void clear(bool clear_meta_data)
        Clear all spectra data and meta data (if called with True)
        """
        ...
    
    @overload
    def updateRanges(self, ) -> None:
        """
        Cython signature: void updateRanges()
        Recalculate global RT and m/z ranges after changes to the data has been made.
        """
        ...
    
    @overload
    def updateRanges(self, msLevel: int ) -> None:
        """
        Cython signature: void updateRanges(int msLevel)
        Recalculate RT and m/z ranges for a specific MS level
        """
        ...
    
    def reserveSpaceSpectra(self, s: int ) -> None:
        """
        Cython signature: void reserveSpaceSpectra(size_t s)
        """
        ...
    
    def reserveSpaceChromatograms(self, s: int ) -> None:
        """
        Cython signature: void reserveSpaceChromatograms(size_t s)
        """
        ...
    
    def getSize(self) -> int:
        """
        Cython signature: uint64_t getSize()
        Returns the total number of peaks
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: int size()
        """
        ...
    
    def resize(self, s: int ) -> None:
        """
        Cython signature: void resize(size_t s)
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        """
        ...
    
    def reserve(self, s: int ) -> None:
        """
        Cython signature: void reserve(size_t s)
        """
        ...
    
    def getNrSpectra(self) -> int:
        """
        Cython signature: size_t getNrSpectra()
        Returns the number of MS spectra
        """
        ...
    
    def getNrChromatograms(self) -> int:
        """
        Cython signature: size_t getNrChromatograms()
        Returns the number of chromatograms
        """
        ...
    
    @overload
    def sortSpectra(self, sort_mz: bool ) -> None:
        """
        Cython signature: void sortSpectra(bool sort_mz)
        Sorts spectra by RT. If sort_mz=True also sort each peak in a spectrum by m/z
        """
        ...
    
    @overload
    def sortSpectra(self, ) -> None:
        """
        Cython signature: void sortSpectra()
        """
        ...
    
    @overload
    def sortChromatograms(self, sort_rt: bool ) -> None:
        """
        Cython signature: void sortChromatograms(bool sort_rt)
        Sorts chromatograms by m/z. If sort_rt=True also sort each chromatogram RT
        """
        ...
    
    @overload
    def sortChromatograms(self, ) -> None:
        """
        Cython signature: void sortChromatograms()
        """
        ...
    
    @overload
    def isSorted(self, check_mz: bool ) -> bool:
        """
        Cython signature: bool isSorted(bool check_mz)
        Checks if all spectra are sorted with respect to ascending RT
        """
        ...
    
    @overload
    def isSorted(self, ) -> bool:
        """
        Cython signature: bool isSorted()
        """
        ...
    
    def getPrimaryMSRunPath(self, toFill: List[bytes] ) -> None:
        """
        Cython signature: void getPrimaryMSRunPath(StringList & toFill)
        References to the first MS file(s) after conversions. Used to trace results back to original data.
        """
        ...
    
    def swap(self, in_0: MSExperiment ) -> None:
        """
        Cython signature: void swap(MSExperiment)
        """
        ...
    
    def reset(self) -> None:
        """
        Cython signature: void reset()
        """
        ...
    
    def clearMetaDataArrays(self) -> bool:
        """
        Cython signature: bool clearMetaDataArrays()
        """
        ...
    
    def getPrecursorSpectrum(self, zero_based_index: int ) -> int:
        """
        Cython signature: int getPrecursorSpectrum(int zero_based_index)
        Returns the index of the precursor spectrum for spectrum at index @p zero_based_index
        """
        ...
    
    def getSourceFiles(self) -> List[SourceFile]:
        """
        Cython signature: libcpp_vector[SourceFile] getSourceFiles()
        Returns a reference to the source data file
        """
        ...
    
    def setSourceFiles(self, source_files: List[SourceFile] ) -> None:
        """
        Cython signature: void setSourceFiles(libcpp_vector[SourceFile] source_files)
        Sets the source data file
        """
        ...
    
    def getDateTime(self) -> DateTime:
        """
        Cython signature: DateTime getDateTime()
        Returns the date the experiment was performed
        """
        ...
    
    def setDateTime(self, date_time: DateTime ) -> None:
        """
        Cython signature: void setDateTime(DateTime date_time)
        Sets the date the experiment was performed
        """
        ...
    
    def getSample(self) -> Sample:
        """
        Cython signature: Sample getSample()
        Returns a reference to the sample description
        """
        ...
    
    def setSample(self, sample: Sample ) -> None:
        """
        Cython signature: void setSample(Sample sample)
        Sets the sample description
        """
        ...
    
    def getContacts(self) -> List[ContactPerson]:
        """
        Cython signature: libcpp_vector[ContactPerson] getContacts()
        Returns a reference to the list of contact persons
        """
        ...
    
    def setContacts(self, contacts: List[ContactPerson] ) -> None:
        """
        Cython signature: void setContacts(libcpp_vector[ContactPerson] contacts)
        Sets the list of contact persons
        """
        ...
    
    def getInstrument(self) -> Instrument:
        """
        Cython signature: Instrument getInstrument()
        Returns a reference to the MS instrument description
        """
        ...
    
    def setInstrument(self, instrument: Instrument ) -> None:
        """
        Cython signature: void setInstrument(Instrument instrument)
        Sets the MS instrument description
        """
        ...
    
    def getHPLC(self) -> HPLC:
        """
        Cython signature: HPLC getHPLC()
        Returns a reference to the description of the HPLC run
        """
        ...
    
    def setHPLC(self, hplc: HPLC ) -> None:
        """
        Cython signature: void setHPLC(HPLC hplc)
        Sets the description of the HPLC run
        """
        ...
    
    def getComment(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getComment()
        Returns the free-text comment
        """
        ...
    
    def setComment(self, comment: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setComment(String comment)
        Sets the free-text comment
        """
        ...
    
    def getProteinIdentifications(self) -> List[ProteinIdentification]:
        """
        Cython signature: libcpp_vector[ProteinIdentification] getProteinIdentifications()
        Returns a reference to the protein ProteinIdentification vector
        """
        ...
    
    def setProteinIdentifications(self, protein_identifications: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void setProteinIdentifications(libcpp_vector[ProteinIdentification] protein_identifications)
        Sets the protein ProteinIdentification vector
        """
        ...
    
    def getFractionIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFractionIdentifier()
        Returns fraction identifier
        """
        ...
    
    def setFractionIdentifier(self, fraction_identifier: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFractionIdentifier(String fraction_identifier)
        Sets the fraction identifier
        """
        ...
    
    def setIdentifier(self, id: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(String id)
        Sets document identifier (e.g. an LSID)
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        Retrieve document identifier (e.g. an LSID)
        """
        ...
    
    def setLoadedFileType(self, file_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setLoadedFileType(String file_name)
        Sets the file_type according to the type of the file loaded from, preferably done whilst loading
        """
        ...
    
    def getLoadedFileType(self) -> int:
        """
        Cython signature: int getLoadedFileType()
        Returns the file_type (e.g. featureXML, consensusXML, mzData, mzXML, mzML, ...) of the file loaded
        """
        ...
    
    def setLoadedFilePath(self, file_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setLoadedFilePath(String file_name)
        Sets the file_name according to absolute path of the file loaded, preferably done whilst loading
        """
        ...
    
    def getLoadedFilePath(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getLoadedFilePath()
        Returns the file_name which is the absolute path to the file loaded
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def getMinRT(self) -> float:
        """
        Cython signature: double getMinRT()
        Returns the minimum RT
        """
        ...
    
    def getMaxRT(self) -> float:
        """
        Cython signature: double getMaxRT()
        Returns the maximum RT
        """
        ...
    
    def getMinMZ(self) -> float:
        """
        Cython signature: double getMinMZ()
        Returns the minimum m/z
        """
        ...
    
    def getMaxMZ(self) -> float:
        """
        Cython signature: double getMaxMZ()
        Returns the maximum m/z
        """
        ...
    
    def getMinIntensity(self) -> float:
        """
        Cython signature: double getMinIntensity()
        Returns the minimum intensity
        """
        ...
    
    def getMaxIntensity(self) -> float:
        """
        Cython signature: double getMaxIntensity()
        Returns the maximum intensity
        """
        ...
    
    def clearRanges(self) -> None:
        """
        Cython signature: void clearRanges()
        Resets all range dimensions as empty
        """
        ...
    
    def __richcmp__(self, other: MSExperiment, op: int) -> Any:
        ...
    
    def __iter__(self) -> MSSpectrum:
       ... 


class MapConversion:
    """
    Cython implementation of _MapConversion

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MapConversion.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MapConversion()
        """
        ...
    
    @overload
    def __init__(self, in_0: MapConversion ) -> None:
        """
        Cython signature: void MapConversion(MapConversion &)
        """
        ...
    
    @overload
    def convert(self, input_map_index: int , input_map: FeatureMap , output_map: ConsensusMap , n: int ) -> None:
        """
        Cython signature: void convert(uint64_t input_map_index, FeatureMap input_map, ConsensusMap & output_map, size_t n)
        """
        ...
    
    @overload
    def convert(self, input_map_index: int , input_map: MSExperiment , output_map: ConsensusMap , n: int ) -> None:
        """
        Cython signature: void convert(uint64_t input_map_index, MSExperiment & input_map, ConsensusMap & output_map, size_t n)
        """
        ...
    
    @overload
    def convert(self, input_map: ConsensusMap , keep_uids: bool , output_map: FeatureMap ) -> None:
        """
        Cython signature: void convert(ConsensusMap input_map, bool keep_uids, FeatureMap & output_map)
        """
        ... 


class MassDecomposition:
    """
    Cython implementation of _MassDecomposition

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MassDecomposition.html>`_

    Class represents a decomposition of a mass into amino acids
    
    This class represents a mass decomposition into amino acids. A
    decomposition are amino acids given with frequencies which add
    up to a specific mass.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MassDecomposition()
        """
        ...
    
    @overload
    def __init__(self, in_0: MassDecomposition ) -> None:
        """
        Cython signature: void MassDecomposition(MassDecomposition &)
        """
        ...
    
    @overload
    def __init__(self, deco: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void MassDecomposition(const String & deco)
        """
        ...
    
    def toString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the decomposition as a string
        """
        ...
    
    def toExpandedString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toExpandedString()
        Returns the decomposition as a string; instead of frequencies the amino acids are repeated
        """
        ...
    
    def getNumberOfMaxAA(self) -> int:
        """
        Cython signature: size_t getNumberOfMaxAA()
        Returns the max frequency of this composition
        """
        ...
    
    def containsTag(self, tag: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool containsTag(const String & tag)
        Returns true if tag is contained in the mass decomposition
        """
        ...
    
    def compatible(self, deco: MassDecomposition ) -> bool:
        """
        Cython signature: bool compatible(MassDecomposition & deco)
        Returns true if the mass decomposition if contained in this instance
        """
        ...
    
    def __str__(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the decomposition as a string
        """
        ... 


class MetaInfo:
    """
    Cython implementation of _MetaInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaInfo.html>`_

    A Type-Name-Value tuple class
    
    MetaInfo maps an index (an integer corresponding to a string) to
    DataValue objects.  The mapping of strings to the index is performed by
    the MetaInfoRegistry, which can be accessed by the method registry()
    
    There are two versions of nearly all members. One which operates with a
    string name and another one which operates on an index. The index version
    is always faster, as it does not need to look up the index corresponding
    to the string in the MetaInfoRegistry
    
    If you wish to add a MetaInfo member to a class, consider deriving that
    class from MetaInfoInterface, instead of simply adding MetaInfo as
    member. MetaInfoInterface implements a full interface to a MetaInfo
    member and is more memory efficient if no meta info gets added
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaInfo()
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaInfo ) -> None:
        """
        Cython signature: void MetaInfo(MetaInfo &)
        """
        ...
    
    @overload
    def getValue(self, name: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getValue(String name)
        Returns the value corresponding to a string
        """
        ...
    
    @overload
    def getValue(self, index: int ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getValue(unsigned int index)
        Returns the value corresponding to an index
        """
        ...
    
    @overload
    def getValue(self, name: Union[bytes, str, String] , default_value: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getValue(String name, DataValue default_value)
        Returns the value corresponding to a string
        """
        ...
    
    @overload
    def getValue(self, index: int , default_value: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getValue(unsigned int index, DataValue default_value)
        Returns the value corresponding to an index
        """
        ...
    
    @overload
    def exists(self, name: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool exists(String name)
        Returns if this MetaInfo is set
        """
        ...
    
    @overload
    def exists(self, index: int ) -> bool:
        """
        Cython signature: bool exists(unsigned int index)
        Returns if this MetaInfo is set
        """
        ...
    
    @overload
    def setValue(self, name: Union[bytes, str, String] , value: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setValue(String name, DataValue value)
        Sets the DataValue corresponding to a name
        """
        ...
    
    @overload
    def setValue(self, index: int , value: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setValue(unsigned int index, DataValue value)
        Sets the DataValue corresponding to an index
        """
        ...
    
    @overload
    def removeValue(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeValue(String name)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    @overload
    def removeValue(self, index: int ) -> None:
        """
        Cython signature: void removeValue(unsigned int index)
        Removes the DataValue corresponding to `index` if it exists
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getKeysAsIntegers(self, keys: List[int] ) -> None:
        """
        Cython signature: void getKeysAsIntegers(libcpp_vector[unsigned int] & keys)
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        Removes all meta values
        """
        ...
    
    def registry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry registry()
        """
        ... 


class MetaInfoInterface:
    """
    Cython implementation of _MetaInfoInterface

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaInfoInterface.html>`_

    Interface for classes that can store arbitrary meta information
    (Type-Name-Value tuples).
    
    MetaInfoInterface is a base class for all classes that use one MetaInfo
    object as member.  If you want to add meta information to a class, let it
    publicly inherit the MetaInfoInterface.  Meta information is an array of
    Type-Name-Value tuples.
    
    Usage:
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaInfoInterface()
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaInfoInterface ) -> None:
        """
        Cython signature: void MetaInfoInterface(MetaInfoInterface &)
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def __richcmp__(self, other: MetaInfoInterface, op: int) -> Any:
        ... 


class MetaboTargetedTargetDecoy:
    """
    Cython implementation of _MetaboTargetedTargetDecoy

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaboTargetedTargetDecoy.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaboTargetedTargetDecoy()
        Resolve overlapping fragments and missing decoys for experimental specific decoy generation in targeted/pseudo targeted metabolomics
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaboTargetedTargetDecoy ) -> None:
        """
        Cython signature: void MetaboTargetedTargetDecoy(MetaboTargetedTargetDecoy &)
        """
        ...
    
    def constructTargetDecoyMassMapping(self, t_exp: TargetedExperiment ) -> List[MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping]:
        """
        Cython signature: libcpp_vector[MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping] constructTargetDecoyMassMapping(TargetedExperiment & t_exp)
        Constructs a mass mapping of targets and decoys using the unique m_id identifier
        
        
        :param t_exp: TransitionExperiment holds compound and transition information used for the mapping
        """
        ...
    
    def resolveOverlappingTargetDecoyMassesByDecoyMassShift(self, t_exp: TargetedExperiment , mappings: List[MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping] , mass_to_add: float , mz_tol: float , mz_tol_unit: String ) -> None:
        """
        Cython signature: void resolveOverlappingTargetDecoyMassesByDecoyMassShift(TargetedExperiment & t_exp, libcpp_vector[MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping] & mappings, double & mass_to_add, double & mz_tol, String & mz_tol_unit)
        Resolves overlapping target and decoy transition masses by adding a specifiable mass (e.g. CH2) to the overlapping decoy fragment
        
        
        :param t_exp: TransitionExperiment holds compound and transition information
        :param mappings: Map of identifier to target and decoy masses
        :param mass_to_add: (e.g. CH2)
        :param mz_tol: m/z tolerarance for target and decoy transition masses to be considered overlapping
        :param mz_tol_unit: m/z tolerance unit
        """
        ...
    
    def generateMissingDecoysByMassShift(self, t_exp: TargetedExperiment , mappings: List[MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping] , mass_to_add: float ) -> None:
        """
        Cython signature: void generateMissingDecoysByMassShift(TargetedExperiment & t_exp, libcpp_vector[MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping] & mappings, double & mass_to_add)
        Generate a decoy for targets where fragmentation tree re-rooting was not possible, by adding a specifiable mass to the target fragments
        
        
        :param t_exp: TransitionExperiment holds compound and transition information
        :param mappings: Map of identifier to target and decoy masses
        :param mass_to_add: The maximum number of transitions required per assay
        """
        ... 


class MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping:
    """
    Cython implementation of _MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping()
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping ) -> None:
        """
        Cython signature: void MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping(MetaboTargetedTargetDecoy_MetaboTargetDecoyMassMapping &)
        """
        ... 


class MultiplexIsotopicPeakPattern:
    """
    Cython implementation of _MultiplexIsotopicPeakPattern

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MultiplexIsotopicPeakPattern.html>`_
    """
    
    @overload
    def __init__(self, c: int , ppp: int , ms: MultiplexDeltaMasses , msi: int ) -> None:
        """
        Cython signature: void MultiplexIsotopicPeakPattern(int c, int ppp, MultiplexDeltaMasses ms, int msi)
        """
        ...
    
    @overload
    def __init__(self, in_0: MultiplexIsotopicPeakPattern ) -> None:
        """
        Cython signature: void MultiplexIsotopicPeakPattern(MultiplexIsotopicPeakPattern &)
        """
        ...
    
    def getCharge(self) -> int:
        """
        Cython signature: int getCharge()
        Returns charge
        """
        ...
    
    def getPeaksPerPeptide(self) -> int:
        """
        Cython signature: int getPeaksPerPeptide()
        Returns peaks per peptide
        """
        ...
    
    def getMassShifts(self) -> MultiplexDeltaMasses:
        """
        Cython signature: MultiplexDeltaMasses getMassShifts()
        Returns mass shifts
        """
        ...
    
    def getMassShiftIndex(self) -> int:
        """
        Cython signature: int getMassShiftIndex()
        Returns mass shift index
        """
        ...
    
    def getMassShiftCount(self) -> int:
        """
        Cython signature: unsigned int getMassShiftCount()
        Returns number of mass shifts i.e. the number of peptides in the multiplet
        """
        ...
    
    def getMassShiftAt(self, i: int ) -> float:
        """
        Cython signature: double getMassShiftAt(int i)
        Returns mass shift at position i
        """
        ...
    
    def getMZShiftAt(self, i: int ) -> float:
        """
        Cython signature: double getMZShiftAt(int i)
        Returns m/z shift at position i
        """
        ...
    
    def getMZShiftCount(self) -> int:
        """
        Cython signature: unsigned int getMZShiftCount()
        Returns number of m/z shifts
        """
        ... 


class NucleicAcidSpectrumGenerator:
    """
    Cython implementation of _NucleicAcidSpectrumGenerator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1NucleicAcidSpectrumGenerator.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void NucleicAcidSpectrumGenerator()
        """
        ...
    
    @overload
    def __init__(self, in_0: NucleicAcidSpectrumGenerator ) -> None:
        """
        Cython signature: void NucleicAcidSpectrumGenerator(NucleicAcidSpectrumGenerator &)
        """
        ...
    
    def getSpectrum(self, spec: MSSpectrum , oligo: NASequence , min_charge: int , max_charge: int ) -> None:
        """
        Cython signature: void getSpectrum(MSSpectrum & spec, NASequence & oligo, int min_charge, int max_charge)
        Generates a spectrum for a peptide sequence, with the ion types that are set in the tool parameters. If precursor_charge is set to 0 max_charge + 1 will be used
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class OMSSACSVFile:
    """
    Cython implementation of _OMSSACSVFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OMSSACSVFile.html>`_

    File adapter for OMSSACSV files
    
    The files contain the results of the OMSSA algorithm in a comma separated manner. This file adapter is able to
    load the data from such a file into the structures of OpenMS
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OMSSACSVFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: OMSSACSVFile ) -> None:
        """
        Cython signature: void OMSSACSVFile(OMSSACSVFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , protein_identification: ProteinIdentification , id_data: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void load(const String & filename, ProteinIdentification & protein_identification, libcpp_vector[PeptideIdentification] & id_data)
        Loads a OMSSA file
        
        The content of the file is stored in `features`
        
        
        :param filename: The name of the file to read from
        :param protein_identification: The protein ProteinIdentification data
        :param id_data: The peptide ids of the file
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ... 


class OpenPepXLLFAlgorithm:
    """
    Cython implementation of _OpenPepXLLFAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OpenPepXLLFAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OpenPepXLLFAlgorithm()
        """
        ...
    
    @overload
    def __init__(self, in_0: OpenPepXLLFAlgorithm ) -> None:
        """
        Cython signature: void OpenPepXLLFAlgorithm(OpenPepXLLFAlgorithm &)
        """
        ...
    
    def run(self, unprocessed_spectra: MSExperiment , fasta_db: List[FASTAEntry] , protein_ids: List[ProteinIdentification] , peptide_ids: List[PeptideIdentification] , all_top_csms: List[List[CrossLinkSpectrumMatch]] , spectra: MSExperiment ) -> int:
        """
        Cython signature: OpenPepXLLFAlgorithm_ExitCodes run(MSExperiment & unprocessed_spectra, libcpp_vector[FASTAEntry] & fasta_db, libcpp_vector[ProteinIdentification] & protein_ids, libcpp_vector[PeptideIdentification] & peptide_ids, libcpp_vector[libcpp_vector[CrossLinkSpectrumMatch]] & all_top_csms, MSExperiment & spectra)
        Performs the main function of this class, the search for cross-linked peptides
        
        
        :param unprocessed_spectra: The input PeakMap of experimental spectra
        :param fasta_db: The protein database containing targets and decoys
        :param protein_ids: A result vector containing search settings. Should contain one PeptideIdentification
        :param peptide_ids: A result vector containing cross-link spectrum matches as PeptideIdentifications and PeptideHits. Should be empty
        :param all_top_csms: A result vector containing cross-link spectrum matches as CrossLinkSpectrumMatches. Should be empty. This is only necessary for writing out xQuest type spectrum files
        :param spectra: A result vector containing the input spectra after preprocessing and filtering. Should be empty. This is only necessary for writing out xQuest type spectrum files
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ...
    OpenPepXLLFAlgorithm_ExitCodes : __OpenPepXLLFAlgorithm_ExitCodes 


class OpenSwathDataAccessHelper:
    """
    Cython implementation of _OpenSwathDataAccessHelper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OpenSwathDataAccessHelper.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OpenSwathDataAccessHelper()
        """
        ...
    
    @overload
    def __init__(self, in_0: OpenSwathDataAccessHelper ) -> None:
        """
        Cython signature: void OpenSwathDataAccessHelper(OpenSwathDataAccessHelper &)
        """
        ...
    
    def convertToOpenMSSpectrum(self, sptr: OSSpectrum , spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void convertToOpenMSSpectrum(shared_ptr[OSSpectrum] sptr, MSSpectrum & spectrum)
        Converts a SpectrumPtr to an OpenMS Spectrum
        """
        ...
    
    def convertToOpenMSChromatogram(self, cptr: OSChromatogram , chromatogram: MSChromatogram ) -> None:
        """
        Cython signature: void convertToOpenMSChromatogram(shared_ptr[OSChromatogram] cptr, MSChromatogram & chromatogram)
        Converts a ChromatogramPtr to an OpenMS Chromatogram
        """
        ...
    
    def convertToOpenMSChromatogramFilter(self, chromatogram: MSChromatogram , cptr: OSChromatogram , rt_min: float , rt_max: float ) -> None:
        """
        Cython signature: void convertToOpenMSChromatogramFilter(MSChromatogram & chromatogram, shared_ptr[OSChromatogram] cptr, double rt_min, double rt_max)
        """
        ...
    
    def convertTargetedExp(self, transition_exp_: TargetedExperiment , transition_exp: LightTargetedExperiment ) -> None:
        """
        Cython signature: void convertTargetedExp(TargetedExperiment & transition_exp_, LightTargetedExperiment & transition_exp)
        Converts from the OpenMS TargetedExperiment to the OpenMs LightTargetedExperiment
        """
        ...
    
    def convertPeptideToAASequence(self, peptide: LightCompound , aa_sequence: AASequence ) -> None:
        """
        Cython signature: void convertPeptideToAASequence(LightCompound & peptide, AASequence & aa_sequence)
        Converts from the LightCompound to an OpenMS AASequence (with correct modifications)
        """
        ...
    
    def convertTargetedCompound(self, pep: Peptide , p: LightCompound ) -> None:
        """
        Cython signature: void convertTargetedCompound(Peptide pep, LightCompound & p)
        Converts from the OpenMS TargetedExperiment Peptide to the LightTargetedExperiment Peptide
        """
        ... 


class OpenSwathOSWWriter:
    """
    Cython implementation of _OpenSwathOSWWriter

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OpenSwathOSWWriter.html>`_
    """
    
    @overload
    def __init__(self, output_filename: Union[bytes, str, String] , run_id: int , input_filename: Union[bytes, str, String] , uis_scores: bool ) -> None:
        """
        Cython signature: void OpenSwathOSWWriter(String output_filename, uint64_t run_id, String input_filename, bool uis_scores)
        """
        ...
    
    @overload
    def __init__(self, in_0: OpenSwathOSWWriter ) -> None:
        """
        Cython signature: void OpenSwathOSWWriter(OpenSwathOSWWriter &)
        """
        ...
    
    def isActive(self) -> bool:
        """
        Cython signature: bool isActive()
        """
        ...
    
    def writeHeader(self) -> None:
        """
        Cython signature: void writeHeader()
        Initializes file by generating SQLite tables
        """
        ...
    
    def prepareLine(self, compound: LightCompound , tr: LightTransition , output: FeatureMap , id_: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String prepareLine(LightCompound & compound, LightTransition * tr, FeatureMap & output, String id_)
        Prepare a single line (feature) for output
        
        The result can be flushed to disk using writeLines (either line by line or after collecting several lines)
        
        
        :param pep: The compound (peptide/metabolite) used for extraction
        :param transition: The transition used for extraction
        :param output: The feature map containing all features (each feature will generate one entry in the output)
        :param id: The transition group identifier (peptide/metabolite id)
        :return: A String to be written using writeLines
        """
        ...
    
    def writeLines(self, to_osw_output: List[bytes] ) -> None:
        """
        Cython signature: void writeLines(libcpp_vector[String] to_osw_output)
        Write data to disk
        
        Takes a set of pre-prepared data statements from prepareLine and flushes them to disk
        
        
        :param to_osw_output: Statements generated by prepareLine
        """
        ... 


class Param:
    """
    Cython implementation of _Param

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Param.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Param()
        """
        ...
    
    @overload
    def __init__(self, in_0: Param ) -> None:
        """
        Cython signature: void Param(Param &)
        """
        ...
    
    @overload
    def setValue(self, key: Union[bytes, str] , val: Union[int, float, bytes, str, List[int], List[float], List[bytes]] , desc: Union[bytes, str] , tags: List[Union[bytes, str]] ) -> None:
        """
        Cython signature: void setValue(libcpp_utf8_string key, ParamValue val, libcpp_utf8_string desc, libcpp_vector[libcpp_utf8_string] tags)
        """
        ...
    
    @overload
    def setValue(self, key: Union[bytes, str] , val: Union[int, float, bytes, str, List[int], List[float], List[bytes]] , desc: Union[bytes, str] ) -> None:
        """
        Cython signature: void setValue(libcpp_utf8_string key, ParamValue val, libcpp_utf8_string desc)
        """
        ...
    
    @overload
    def setValue(self, key: Union[bytes, str] , val: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setValue(libcpp_utf8_string key, ParamValue val)
        """
        ...
    
    def getValue(self, key: Union[bytes, str] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: ParamValue getValue(libcpp_utf8_string key)
        """
        ...
    
    def getValueType(self, key: Union[bytes, str] ) -> int:
        """
        Cython signature: ValueType getValueType(libcpp_utf8_string key)
        """
        ...
    
    def getEntry(self, in_0: Union[bytes, str] ) -> ParamEntry:
        """
        Cython signature: ParamEntry getEntry(libcpp_utf8_string)
        """
        ...
    
    def exists(self, key: Union[bytes, str] ) -> bool:
        """
        Cython signature: bool exists(libcpp_utf8_string key)
        """
        ...
    
    def addTag(self, key: Union[bytes, str] , tag: Union[bytes, str] ) -> None:
        """
        Cython signature: void addTag(libcpp_utf8_string key, libcpp_utf8_string tag)
        """
        ...
    
    def addTags(self, key: Union[bytes, str] , tags: List[Union[bytes, str]] ) -> None:
        """
        Cython signature: void addTags(libcpp_utf8_string key, libcpp_vector[libcpp_utf8_string] tags)
        """
        ...
    
    def hasTag(self, key: Union[bytes, str] , tag: Union[bytes, str] ) -> int:
        """
        Cython signature: int hasTag(libcpp_utf8_string key, libcpp_utf8_string tag)
        """
        ...
    
    def getTags(self, key: Union[bytes, str] ) -> List[bytes]:
        """
        Cython signature: libcpp_vector[libcpp_string] getTags(libcpp_utf8_string key)
        """
        ...
    
    def clearTags(self, key: Union[bytes, str] ) -> None:
        """
        Cython signature: void clearTags(libcpp_utf8_string key)
        """
        ...
    
    def getDescription(self, key: Union[bytes, str] ) -> str:
        """
        Cython signature: libcpp_utf8_output_string getDescription(libcpp_utf8_string key)
        """
        ...
    
    def setSectionDescription(self, key: Union[bytes, str] , desc: Union[bytes, str] ) -> None:
        """
        Cython signature: void setSectionDescription(libcpp_utf8_string key, libcpp_utf8_string desc)
        """
        ...
    
    def getSectionDescription(self, key: Union[bytes, str] ) -> str:
        """
        Cython signature: libcpp_utf8_output_string getSectionDescription(libcpp_utf8_string key)
        """
        ...
    
    def addSection(self, key: Union[bytes, str] , desc: Union[bytes, str] ) -> None:
        """
        Cython signature: void addSection(libcpp_utf8_string key, libcpp_utf8_string desc)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ...
    
    def insert(self, prefix: Union[bytes, str] , param: Param ) -> None:
        """
        Cython signature: void insert(libcpp_utf8_string prefix, Param param)
        """
        ...
    
    def remove(self, key: Union[bytes, str] ) -> None:
        """
        Cython signature: void remove(libcpp_utf8_string key)
        """
        ...
    
    def removeAll(self, prefix: Union[bytes, str] ) -> None:
        """
        Cython signature: void removeAll(libcpp_utf8_string prefix)
        """
        ...
    
    @overload
    def copy(self, prefix: Union[bytes, str] , in_1: bool ) -> Param:
        """
        Cython signature: Param copy(libcpp_utf8_string prefix, bool)
        """
        ...
    
    @overload
    def copy(self, prefix: Union[bytes, str] ) -> Param:
        """
        Cython signature: Param copy(libcpp_utf8_string prefix)
        """
        ...
    
    def merge(self, toMerge: Param ) -> None:
        """
        Cython signature: void merge(Param toMerge)
        """
        ...
    
    @overload
    def setDefaults(self, defaults: Param , prefix: Union[bytes, str] , showMessage: bool ) -> None:
        """
        Cython signature: void setDefaults(Param defaults, libcpp_utf8_string prefix, bool showMessage)
        """
        ...
    
    @overload
    def setDefaults(self, defaults: Param , prefix: Union[bytes, str] ) -> None:
        """
        Cython signature: void setDefaults(Param defaults, libcpp_utf8_string prefix)
        """
        ...
    
    @overload
    def setDefaults(self, defaults: Param ) -> None:
        """
        Cython signature: void setDefaults(Param defaults)
        """
        ...
    
    @overload
    def checkDefaults(self, name: Union[bytes, str] , defaults: Param , prefix: Union[bytes, str] ) -> None:
        """
        Cython signature: void checkDefaults(libcpp_utf8_string name, Param defaults, libcpp_utf8_string prefix)
        """
        ...
    
    @overload
    def checkDefaults(self, name: Union[bytes, str] , defaults: Param ) -> None:
        """
        Cython signature: void checkDefaults(libcpp_utf8_string name, Param defaults)
        """
        ...
    
    def getValidStrings(self, key: Union[bytes, str] ) -> List[Union[bytes, str]]:
        """
        Cython signature: libcpp_vector[libcpp_utf8_string] getValidStrings(libcpp_utf8_string key)
        """
        ...
    
    def setValidStrings(self, key: Union[bytes, str] , strings: List[Union[bytes, str]] ) -> None:
        """
        Cython signature: void setValidStrings(libcpp_utf8_string key, libcpp_vector[libcpp_utf8_string] strings)
        """
        ...
    
    def setMinInt(self, key: Union[bytes, str] , min: int ) -> None:
        """
        Cython signature: void setMinInt(libcpp_utf8_string key, int min)
        """
        ...
    
    def setMaxInt(self, key: Union[bytes, str] , max: int ) -> None:
        """
        Cython signature: void setMaxInt(libcpp_utf8_string key, int max)
        """
        ...
    
    def setMinFloat(self, key: Union[bytes, str] , min: float ) -> None:
        """
        Cython signature: void setMinFloat(libcpp_utf8_string key, double min)
        """
        ...
    
    def setMaxFloat(self, key: Union[bytes, str] , max: float ) -> None:
        """
        Cython signature: void setMaxFloat(libcpp_utf8_string key, double max)
        """
        ...
    
    def __richcmp__(self, other: Param, op: int) -> Any:
        ... 


class PeakIndex:
    """
    Cython implementation of _PeakIndex

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeakIndex.html>`_

    Index of a peak or feature
    
    This struct can be used to store both peak or feature indices
    """
    
    peak: int
    
    spectrum: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeakIndex()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeakIndex ) -> None:
        """
        Cython signature: void PeakIndex(PeakIndex &)
        """
        ...
    
    @overload
    def __init__(self, peak: int ) -> None:
        """
        Cython signature: void PeakIndex(size_t peak)
        """
        ...
    
    @overload
    def __init__(self, spectrum: int , peak: int ) -> None:
        """
        Cython signature: void PeakIndex(size_t spectrum, size_t peak)
        """
        ...
    
    def isValid(self) -> bool:
        """
        Cython signature: bool isValid()
        Returns if the current peak ref is valid
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        Invalidates the current index
        """
        ...
    
    def getFeature(self, map_: FeatureMap ) -> Feature:
        """
        Cython signature: Feature getFeature(FeatureMap & map_)
        Returns the feature (or consensus feature) corresponding to this index
        
        This method is intended for arrays of features e.g. FeatureMap
        
        The main advantage of using this method instead accessing the data directly is that range
        check performed in debug mode
        
        :raises:
          Exception: Precondition is thrown if this index is invalid for the `map` (only in debug mode)
        """
        ...
    
    def getPeak(self, map_: MSExperiment ) -> Peak1D:
        """
        Cython signature: Peak1D getPeak(MSExperiment & map_)
        Returns a peak corresponding to this index
        
        This method is intended for arrays of DSpectra e.g. MSExperiment
        
        The main advantage of using this method instead accessing the data directly is that range
        check performed in debug mode
        
        :raises:
          Exception: Precondition is thrown if this index is invalid for the `map` (only in debug mode)
        """
        ...
    
    def getSpectrum(self, map_: MSExperiment ) -> MSSpectrum:
        """
        Cython signature: MSSpectrum getSpectrum(MSExperiment & map_)
        Returns a spectrum corresponding to this index
        
        This method is intended for arrays of DSpectra e.g. MSExperiment
        
        The main advantage of using this method instead accessing the data directly is that range
        check performed in debug mode
        
        :raises:
          Exception: Precondition is thrown if this index is invalid for the `map` (only in debug mode)
        """
        ...
    
    def __richcmp__(self, other: PeakIndex, op: int) -> Any:
        ... 


class PeptideIdentification:
    """
    Cython implementation of _PeptideIdentification

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeptideIdentification.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeptideIdentification()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeptideIdentification ) -> None:
        """
        Cython signature: void PeptideIdentification(PeptideIdentification &)
        """
        ...
    
    def getHits(self) -> List[PeptideHit]:
        """
        Cython signature: libcpp_vector[PeptideHit] getHits()
        Returns the peptide hits as const
        """
        ...
    
    def insertHit(self, in_0: PeptideHit ) -> None:
        """
        Cython signature: void insertHit(PeptideHit)
        Appends a peptide hit
        """
        ...
    
    def setHits(self, in_0: List[PeptideHit] ) -> None:
        """
        Cython signature: void setHits(libcpp_vector[PeptideHit])
        Sets the peptide hits
        """
        ...
    
    def getSignificanceThreshold(self) -> float:
        """
        Cython signature: double getSignificanceThreshold()
        Returns the peptide significance threshold value
        """
        ...
    
    def setSignificanceThreshold(self, value: float ) -> None:
        """
        Cython signature: void setSignificanceThreshold(double value)
        Setting of the peptide significance threshold value
        """
        ...
    
    def getScoreType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getScoreType()
        """
        ...
    
    def setScoreType(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setScoreType(String)
        """
        ...
    
    def isHigherScoreBetter(self) -> bool:
        """
        Cython signature: bool isHigherScoreBetter()
        """
        ...
    
    def setHigherScoreBetter(self, in_0: bool ) -> None:
        """
        Cython signature: void setHigherScoreBetter(bool)
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        """
        ...
    
    def setIdentifier(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(String)
        """
        ...
    
    def hasMZ(self) -> bool:
        """
        Cython signature: bool hasMZ()
        """
        ...
    
    def getMZ(self) -> float:
        """
        Cython signature: double getMZ()
        """
        ...
    
    def setMZ(self, in_0: float ) -> None:
        """
        Cython signature: void setMZ(double)
        """
        ...
    
    def hasRT(self) -> bool:
        """
        Cython signature: bool hasRT()
        """
        ...
    
    def getRT(self) -> float:
        """
        Cython signature: double getRT()
        """
        ...
    
    def setRT(self, in_0: float ) -> None:
        """
        Cython signature: void setRT(double)
        """
        ...
    
    def getBaseName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getBaseName()
        """
        ...
    
    def setBaseName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setBaseName(String)
        """
        ...
    
    def getExperimentLabel(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getExperimentLabel()
        """
        ...
    
    def setExperimentLabel(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setExperimentLabel(String)
        """
        ...
    
    def assignRanks(self) -> None:
        """
        Cython signature: void assignRanks()
        """
        ...
    
    def sort(self) -> None:
        """
        Cython signature: void sort()
        """
        ...
    
    def sortByRank(self) -> None:
        """
        Cython signature: void sortByRank()
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        """
        ...
    
    def getReferencingHits(self, in_0: List[PeptideHit] , in_1: Set[bytes] ) -> List[PeptideHit]:
        """
        Cython signature: libcpp_vector[PeptideHit] getReferencingHits(libcpp_vector[PeptideHit], libcpp_set[String] &)
        Returns all peptide hits which reference to a given protein accession (i.e. filter by protein accession)
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def __richcmp__(self, other: PeptideIdentification, op: int) -> Any:
        ... 


class ProteaseDigestion:
    """
    Cython implementation of _ProteaseDigestion

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProteaseDigestion.html>`_
      -- Inherits from ['EnzymaticDigestion']

    Class for the enzymatic digestion of proteins
    
    Digestion can be performed using simple regular expressions, e.g. [KR] | [^P] for trypsin.
    Also missed cleavages can be modeled, i.e. adjacent peptides are not cleaved
    due to enzyme malfunction/access restrictions. If n missed cleavages are allowed, all possible resulting
    peptides (cleaved and uncleaved) with up to n missed cleavages are returned.
    Thus no random selection of just n specific missed cleavage sites is performed.
    
    Usage:
    
    .. code-block:: python
    
          from pyopenms import *
          from urllib.request import urlretrieve
          #
          urlretrieve ("http://www.uniprot.org/uniprot/P02769.fasta", "bsa.fasta")
          #
          dig = ProteaseDigestion()
          dig.setEnzyme('Lys-C')
          bsa_string = "".join([l.strip() for l in open("bsa.fasta").readlines()[1:]])
          bsa_oms_string = String(bsa_string) # convert python string to OpenMS::String for further processing
          #
          minlen = 6
          maxlen = 30
          #
          # Using AASequence and digest
          result_digest = []
          result_digest_min_max = []
          bsa_aaseq = AASequence.fromString(bsa_oms_string)
          dig.digest(bsa_aaseq, result_digest)
          dig.digest(bsa_aaseq, result_digest_min_max, minlen, maxlen)
          print(result_digest[4].toString()) # GLVLIAFSQYLQQCPFDEHVK
          print(len(result_digest)) # 57 peptides
          print(result_digest_min_max[4].toString()) # LVNELTEFAK
          print(len(result_digest_min_max)) # 42 peptides
          #
          # Using digestUnmodified without the need for AASequence from the EnzymaticDigestion base class
          result_digest_unmodified = []
          dig.digestUnmodified(StringView(bsa_oms_string), result_digest_unmodified, minlen, maxlen)
          print(result_digest_unmodified[4].getString()) # LVNELTEFAK
          print(len(result_digest_unmodified)) # 42 peptides
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProteaseDigestion()
        """
        ...
    
    @overload
    def __init__(self, in_0: ProteaseDigestion ) -> None:
        """
        Cython signature: void ProteaseDigestion(ProteaseDigestion &)
        """
        ...
    
    @overload
    def setEnzyme(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setEnzyme(String name)
        Sets the enzyme for the digestion (by name)
        """
        ...
    
    @overload
    def setEnzyme(self, enzyme: DigestionEnzyme ) -> None:
        """
        Cython signature: void setEnzyme(DigestionEnzyme * enzyme)
        Sets the enzyme for the digestion
        """
        ...
    
    @overload
    def digest(self, protein: AASequence , output: List[AASequence] ) -> int:
        """
        Cython signature: size_t digest(AASequence & protein, libcpp_vector[AASequence] & output)
        """
        ...
    
    @overload
    def digest(self, protein: AASequence , output: List[AASequence] , min_length: int , max_length: int ) -> int:
        """
        Cython signature: size_t digest(AASequence & protein, libcpp_vector[AASequence] & output, size_t min_length, size_t max_length)
          Performs the enzymatic digestion of a protein.
        
        
          :param protein: Sequence to digest
          :param output: Digestion products (peptides)
          :param min_length: Minimal length of reported products
          :param max_length: Maximal length of reported products (0 = no restriction)
          :return: Number of discarded digestion products (which are not matching length restrictions)
        """
        ...
    
    def peptideCount(self, protein: AASequence ) -> int:
        """
        Cython signature: size_t peptideCount(AASequence & protein)
        Returns the number of peptides a digestion of protein would yield under the current enzyme and missed cleavage settings
        """
        ...
    
    @overload
    def isValidProduct(self, protein: AASequence , pep_pos: int , pep_length: int , ignore_missed_cleavages: bool , methionine_cleavage: bool ) -> bool:
        """
        Cython signature: bool isValidProduct(AASequence protein, size_t pep_pos, size_t pep_length, bool ignore_missed_cleavages, bool methionine_cleavage)
          Variant of EnzymaticDigestion::isValidProduct() with support for n-term protein cleavage and random D|P cleavage
        
          Checks if peptide is a valid digestion product of the enzyme, taking into account specificity and the flags provided here
        
        
          :param protein: Protein sequence
          :param pep_pos: Starting index of potential peptide
          :param pep_length: Length of potential peptide
          :param ignore_missed_cleavages: Do not compare MC's of potential peptide to the maximum allowed MC's
          :param allow_nterm_protein_cleavage: Regard peptide as n-terminal of protein if it starts only at pos=1 or 2 and protein starts with 'M'
          :param allow_random_asp_pro_cleavage: Allow cleavage at D|P sites to count as n/c-terminal
          :return: True if peptide has correct n/c terminals (according to enzyme, specificity and above flags)
        """
        ...
    
    @overload
    def isValidProduct(self, protein: Union[bytes, str, String] , pep_pos: int , pep_length: int , ignore_missed_cleavages: bool , methionine_cleavage: bool ) -> bool:
        """
        Cython signature: bool isValidProduct(String protein, size_t pep_pos, size_t pep_length, bool ignore_missed_cleavages, bool methionine_cleavage)
        Forwards to isValidProduct using protein.toUnmodifiedString()
        """
        ...
    
    @overload
    def isValidProduct(self, sequence: Union[bytes, str, String] , pos: int , length: int , ignore_missed_cleavages: bool ) -> bool:
        """
        Cython signature: bool isValidProduct(String sequence, int pos, int length, bool ignore_missed_cleavages)
        Boolean operator returns true if the peptide fragment starting at position `pos` with length `length` within the sequence `sequence` generated by the current enzyme\n
        Checks if peptide is a valid digestion product of the enzyme, taking into account specificity and the MC flag provided here
        
        
        :param protein: Protein sequence
        :param pep_pos: Starting index of potential peptide
        :param pep_length: Length of potential peptide
        :param ignore_missed_cleavages: Do not compare MC's of potential peptide to the maximum allowed MC's
        :return: True if peptide has correct n/c terminals (according to enzyme, specificity and missed cleavages)
        """
        ...
    
    def getMissedCleavages(self) -> int:
        """
        Cython signature: size_t getMissedCleavages()
        Returns the max. number of allowed missed cleavages for the digestion
        """
        ...
    
    def setMissedCleavages(self, missed_cleavages: int ) -> None:
        """
        Cython signature: void setMissedCleavages(size_t missed_cleavages)
        Sets the max. number of allowed missed cleavages for the digestion (default is 0). This setting is ignored when log model is used
        """
        ...
    
    def countInternalCleavageSites(self, sequence: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t countInternalCleavageSites(String sequence)
        Returns the number of internal cleavage sites for this sequence.
        """
        ...
    
    def getEnzymeName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getEnzymeName()
        Returns the enzyme for the digestion
        """
        ...
    
    def getSpecificity(self) -> int:
        """
        Cython signature: Specificity getSpecificity()
        Returns the specificity for the digestion
        """
        ...
    
    def setSpecificity(self, spec: int ) -> None:
        """
        Cython signature: void setSpecificity(Specificity spec)
        Sets the specificity for the digestion (default is SPEC_FULL)
        """
        ...
    
    def getSpecificityByName(self, name: Union[bytes, str, String] ) -> int:
        """
        Cython signature: Specificity getSpecificityByName(String name)
        Returns the specificity by name. Returns SPEC_UNKNOWN if name is not valid
        """
        ...
    
    def digestUnmodified(self, sequence: StringView , output: List[StringView] , min_length: int , max_length: int ) -> int:
        """
        Cython signature: size_t digestUnmodified(StringView sequence, libcpp_vector[StringView] & output, size_t min_length, size_t max_length)
        Performs the enzymatic digestion of an unmodified sequence\n
        By returning only references into the original string this is very fast
        
        
        :param sequence: Sequence to digest
        :param output: Digestion products
        :param min_length: Minimal length of reported products
        :param max_length: Maximal length of reported products (0 = no restriction)
        :return: Number of discarded digestion products (which are not matching length restrictions)
        """
        ... 


class QTCluster:
    """
    Cython implementation of _QTCluster

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1QTCluster.html>`_
    """
    
    def __init__(self, in_0: QTCluster ) -> None:
        """
        Cython signature: void QTCluster(QTCluster &)
        """
        ...
    
    def getCenterRT(self) -> float:
        """
        Cython signature: double getCenterRT()
        Returns the RT value of the cluster
        """
        ...
    
    def getCenterMZ(self) -> float:
        """
        Cython signature: double getCenterMZ()
        Returns the m/z value of the cluster center
        """
        ...
    
    def getXCoord(self) -> int:
        """
        Cython signature: int getXCoord()
        Returns the x coordinate in the grid
        """
        ...
    
    def getYCoord(self) -> int:
        """
        Cython signature: int getYCoord()
        Returns the y coordinate in the grid
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        Returns the size of the cluster (number of elements, incl. center)
        """
        ...
    
    def getQuality(self) -> float:
        """
        Cython signature: double getQuality()
        Returns the cluster quality and recomputes if necessary
        """
        ...
    
    def getAnnotations(self) -> Set[AASequence]:
        """
        Cython signature: libcpp_set[AASequence] getAnnotations()
        Returns the set of peptide sequences annotated to the cluster center
        """
        ...
    
    def setInvalid(self) -> None:
        """
        Cython signature: void setInvalid()
        Sets current cluster as invalid (also frees some memory)
        """
        ...
    
    def isInvalid(self) -> bool:
        """
        Cython signature: bool isInvalid()
        Whether current cluster is invalid
        """
        ...
    
    def initializeCluster(self) -> None:
        """
        Cython signature: void initializeCluster()
        Has to be called before adding elements (calling
        """
        ...
    
    def finalizeCluster(self) -> None:
        """
        Cython signature: void finalizeCluster()
        Has to be called after adding elements (after calling
        """
        ...
    
    def __richcmp__(self, other: QTCluster, op: int) -> Any:
        ... 


class QcMLFile:
    """
    Cython implementation of _QcMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1QcMLFile.html>`_
      -- Inherits from ['XMLHandler', 'XMLFile', 'ProgressLogger']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void QcMLFile()
        """
        ...
    
    def exportIDstats(self, filename: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String exportIDstats(const String & filename)
        """
        ...
    
    def addRunQualityParameter(self, r: Union[bytes, str, String] , qp: QualityParameter ) -> None:
        """
        Cython signature: void addRunQualityParameter(String r, QualityParameter qp)
        Adds a QualityParameter to run by the name r
        """
        ...
    
    def addRunAttachment(self, r: Union[bytes, str, String] , at: Attachment ) -> None:
        """
        Cython signature: void addRunAttachment(String r, Attachment at)
        Adds a attachment to run by the name r
        """
        ...
    
    def addSetQualityParameter(self, r: Union[bytes, str, String] , qp: QualityParameter ) -> None:
        """
        Cython signature: void addSetQualityParameter(String r, QualityParameter qp)
        Adds a QualityParameter to set by the name r
        """
        ...
    
    def addSetAttachment(self, r: Union[bytes, str, String] , at: Attachment ) -> None:
        """
        Cython signature: void addSetAttachment(String r, Attachment at)
        Adds a attachment to set by the name r
        """
        ...
    
    @overload
    def removeAttachment(self, r: Union[bytes, str, String] , ids: List[bytes] , at: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeAttachment(String r, libcpp_vector[String] & ids, String at)
        Removes attachments referencing an id given in ids, from run/set r. All attachments if no attachment name is given with at
        """
        ...
    
    @overload
    def removeAttachment(self, r: Union[bytes, str, String] , at: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeAttachment(String r, String at)
        Removes attachment with cv accession at from run/set r
        """
        ...
    
    def removeAllAttachments(self, at: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeAllAttachments(String at)
        Removes attachment with cv accession at from all runs/sets
        """
        ...
    
    def removeQualityParameter(self, r: Union[bytes, str, String] , ids: List[bytes] ) -> None:
        """
        Cython signature: void removeQualityParameter(String r, libcpp_vector[String] & ids)
        Removes QualityParameter going by one of the ID attributes given in ids
        """
        ...
    
    def merge(self, addendum: QcMLFile , setname: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void merge(QcMLFile & addendum, String setname)
        Merges the given QCFile into this one
        """
        ...
    
    def collectSetParameter(self, setname: Union[bytes, str, String] , qp: Union[bytes, str, String] , ret: List[bytes] ) -> None:
        """
        Cython signature: void collectSetParameter(String setname, String qp, libcpp_vector[String] & ret)
        Collects the values of given QPs (as CVid) of the given set
        """
        ...
    
    def exportAttachment(self, filename: Union[bytes, str, String] , qpname: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String exportAttachment(String filename, String qpname)
        Returns a String of a tab separated rows if found empty string else from run/set by the name filename of the qualityparameter by the name qpname
        """
        ...
    
    def getRunNames(self, ids: List[bytes] ) -> None:
        """
        Cython signature: void getRunNames(libcpp_vector[String] & ids)
        Gives the names of the registered runs in the vector ids
        """
        ...
    
    def existsRun(self, filename: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool existsRun(String filename)
        Returns true if the given run id is present in this file, if checkname is true it also checks the names
        """
        ...
    
    def existsSet(self, filename: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool existsSet(String filename)
        Returns true if the given set id is present in this file, if checkname is true it also checks the names
        """
        ...
    
    def existsRunQualityParameter(self, filename: Union[bytes, str, String] , qpname: Union[bytes, str, String] , ids: List[bytes] ) -> None:
        """
        Cython signature: void existsRunQualityParameter(String filename, String qpname, libcpp_vector[String] & ids)
        Returns the ids of the parameter name given if found in given run empty else
        """
        ...
    
    def existsSetQualityParameter(self, filename: Union[bytes, str, String] , qpname: Union[bytes, str, String] , ids: List[bytes] ) -> None:
        """
        Cython signature: void existsSetQualityParameter(String filename, String qpname, libcpp_vector[String] & ids)
        Returns the ids of the parameter name given if found in given set, empty else
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void store(const String & filename)
        Store the qcML file
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void load(const String & filename)
        Load a QCFile
        """
        ...
    
    def registerRun(self, id_: Union[bytes, str, String] , name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void registerRun(String id_, String name)
        Registers a run in the qcml file with the respective mappings
        """
        ...
    
    def registerSet(self, id_: Union[bytes, str, String] , name: Union[bytes, str, String] , names: Set[bytes] ) -> None:
        """
        Cython signature: void registerSet(String id_, String name, libcpp_set[String] & names)
        Registers a set in the qcml file with the respective mappings
        """
        ...
    
    def exportQP(self, filename: Union[bytes, str, String] , qpname: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String exportQP(String filename, String qpname)
        Returns a String value in quotation of a QualityParameter by the name qpname in run/set by the name filename
        """
        ...
    
    def exportQPs(self, filename: Union[bytes, str, String] , qpnames: List[bytes] ) -> Union[bytes, str, String]:
        """
        Cython signature: String exportQPs(String filename, StringList qpnames)
        Returns a String of a tab separated QualityParameter by the name qpname in run/set by the name filename
        """
        ...
    
    def getRunIDs(self, ids: List[bytes] ) -> None:
        """
        Cython signature: void getRunIDs(libcpp_vector[String] & ids)
        Gives the ids of the registered runs in the vector ids
        """
        ...
    
    def reset(self) -> None:
        """
        Cython signature: void reset()
        """
        ...
    
    def error(self, mode: int , msg: Union[bytes, str, String] , line: int , column: int ) -> None:
        """
        Cython signature: void error(ActionMode mode, const String & msg, unsigned int line, unsigned int column)
        """
        ...
    
    def warning(self, mode: int , msg: Union[bytes, str, String] , line: int , column: int ) -> None:
        """
        Cython signature: void warning(ActionMode mode, const String & msg, unsigned int line, unsigned int column)
        """
        ...
    
    def getVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVersion()
        Return the version of the schema
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class QualityParameter:
    """
    Cython implementation of _QualityParameter

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1QualityParameter.html>`_
    """
    
    name: Union[bytes, str, String]
    
    id: Union[bytes, str, String]
    
    value: Union[bytes, str, String]
    
    cvRef: Union[bytes, str, String]
    
    cvAcc: Union[bytes, str, String]
    
    unitRef: Union[bytes, str, String]
    
    unitAcc: Union[bytes, str, String]
    
    flag: Union[bytes, str, String]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void QualityParameter()
        """
        ...
    
    @overload
    def __init__(self, in_0: QualityParameter ) -> None:
        """
        Cython signature: void QualityParameter(QualityParameter &)
        """
        ...
    
    def toXMLString(self, indentation_level: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String toXMLString(unsigned int indentation_level)
        """
        ...
    
    def __richcmp__(self, other: QualityParameter, op: int) -> Any:
        ... 


class Ratio:
    """
    Cython implementation of _Ratio

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Ratio.html>`_
    """
    
    ratio_value_: float
    
    denominator_ref_: Union[bytes, str, String]
    
    numerator_ref_: Union[bytes, str, String]
    
    description_: List[bytes]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Ratio()
        """
        ...
    
    @overload
    def __init__(self, rhs: Ratio ) -> None:
        """
        Cython signature: void Ratio(Ratio rhs)
        """
        ... 


class SequestOutfile:
    """
    Cython implementation of _SequestOutfile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SequestOutfile.html>`_

    Representation of a Sequest output file
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SequestOutfile()
        Representation of a Sequest output file
        """
        ...
    
    @overload
    def __init__(self, in_0: SequestOutfile ) -> None:
        """
        Cython signature: void SequestOutfile(SequestOutfile &)
        """
        ...
    
    def load(self, result_filename: Union[bytes, str, String] , peptide_identifications: List[PeptideIdentification] , protein_identification: ProteinIdentification , p_value_threshold: float , pvalues: List[float] , database: Union[bytes, str, String] , ignore_proteins_per_peptide: bool ) -> None:
        """
        Cython signature: void load(const String & result_filename, libcpp_vector[PeptideIdentification] & peptide_identifications, ProteinIdentification & protein_identification, double p_value_threshold, libcpp_vector[double] & pvalues, const String & database, bool ignore_proteins_per_peptide)
        Loads data from a Sequest outfile
        
        :param result_filename: The file to be loaded
        :param peptide_identifications: The identifications
        :param protein_identification: The protein identifications
        :param p_value_threshold: The significance level (for the peptide hit scores)
        :param pvalues: A list with the pvalues of the peptides (pvalues computed with peptide prophet)
        :param database: The database used for the search
        :param ignore_proteins_per_peptide: This is a hack to deal with files that use a suffix like "+1" in column "Reference", but do not actually list extra protein references in subsequent lines
        """
        ...
    
    def getColumns(self, line: Union[bytes, str, String] , substrings: List[bytes] , number_of_columns: int , reference_column: int ) -> bool:
        """
        Cython signature: bool getColumns(const String & line, libcpp_vector[String] & substrings, size_t number_of_columns, size_t reference_column)
        Retrieves columns from a Sequest outfile line
        """
        ...
    
    def getACAndACType(self, line: Union[bytes, str, String] , accession: String , accession_type: String ) -> None:
        """
        Cython signature: void getACAndACType(String line, String & accession, String & accession_type)
        Retrieves the accession type and accession number from a protein description line
        """
        ...
    
    def __richcmp__(self, other: SequestOutfile, op: int) -> Any:
        ... 


class SignalToNoiseEstimatorMeanIterative:
    """
    Cython implementation of _SignalToNoiseEstimatorMeanIterative[_MSSpectrum]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SignalToNoiseEstimatorMeanIterative[_MSSpectrum].html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SignalToNoiseEstimatorMeanIterative()
        """
        ...
    
    @overload
    def __init__(self, in_0: SignalToNoiseEstimatorMeanIterative ) -> None:
        """
        Cython signature: void SignalToNoiseEstimatorMeanIterative(SignalToNoiseEstimatorMeanIterative &)
        """
        ...
    
    def init(self, c: MSSpectrum ) -> None:
        """
        Cython signature: void init(MSSpectrum & c)
        """
        ...
    
    def getSignalToNoise(self, index: int ) -> float:
        """
        Cython signature: double getSignalToNoise(size_t index)
        """
        ...
    IntensityThresholdCalculation : __IntensityThresholdCalculation 


class SiriusFragmentAnnotation:
    """
    Cython implementation of _SiriusFragmentAnnotation

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SiriusFragmentAnnotation.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SiriusFragmentAnnotation()
        """
        ...
    
    @overload
    def __init__(self, in_0: SiriusFragmentAnnotation ) -> None:
        """
        Cython signature: void SiriusFragmentAnnotation(SiriusFragmentAnnotation &)
        """
        ...
    
    def extractAnnotationsFromSiriusFile(self, path_to_sirius_workspace: String , max_rank: int , decoy: bool , use_exact_mass: bool ) -> List[MSSpectrum]:
        """
        Cython signature: libcpp_vector[MSSpectrum] extractAnnotationsFromSiriusFile(String & path_to_sirius_workspace, size_t max_rank, bool decoy, bool use_exact_mass)
        """
        ...
    
    def extractAndResolveSiriusAnnotations(self, sirius_workspace_subdirs: List[bytes] , score_threshold: float , use_exact_mass: bool , decoy_generation: bool ) -> List[SiriusFragmentAnnotation_SiriusTargetDecoySpectra]:
        """
        Cython signature: libcpp_vector[SiriusFragmentAnnotation_SiriusTargetDecoySpectra] extractAndResolveSiriusAnnotations(libcpp_vector[String] & sirius_workspace_subdirs, double score_threshold, bool use_exact_mass, bool decoy_generation)
        """
        ...
    
    def extract_columnname_to_columnindex(self, csvfile: CsvFile ) -> Dict[bytes, int]:
        """
        Cython signature: libcpp_map[libcpp_string,size_t] extract_columnname_to_columnindex(CsvFile & csvfile)
        """
        ... 


class SiriusFragmentAnnotation_SiriusTargetDecoySpectra:
    """
    Cython implementation of _SiriusFragmentAnnotation_SiriusTargetDecoySpectra

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SiriusFragmentAnnotation_SiriusTargetDecoySpectra.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SiriusFragmentAnnotation_SiriusTargetDecoySpectra()
        """
        ...
    
    @overload
    def __init__(self, in_0: SiriusFragmentAnnotation_SiriusTargetDecoySpectra ) -> None:
        """
        Cython signature: void SiriusFragmentAnnotation_SiriusTargetDecoySpectra(SiriusFragmentAnnotation_SiriusTargetDecoySpectra &)
        """
        ... 


class Software:
    """
    Cython implementation of _Software

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Software.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Software()
        """
        ...
    
    @overload
    def __init__(self, in_0: Software ) -> None:
        """
        Cython signature: void Software(Software &)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the software
        """
        ...
    
    def getVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVersion()
        Returns the software version
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String)
        Sets the name of the software
        """
        ...
    
    def setVersion(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setVersion(String)
        Sets the software version
        """
        ... 


class SourceFile:
    """
    Cython implementation of _SourceFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SourceFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SourceFile()
        Description of a file location, used to store the origin of (meta) data
        """
        ...
    
    @overload
    def __init__(self, in_0: SourceFile ) -> None:
        """
        Cython signature: void SourceFile(SourceFile &)
        """
        ...
    
    def getNameOfFile(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNameOfFile()
        Returns the file name
        """
        ...
    
    def setNameOfFile(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNameOfFile(String)
        Sets the file name
        """
        ...
    
    def getPathToFile(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getPathToFile()
        Returns the file path
        """
        ...
    
    def setPathToFile(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setPathToFile(String)
        Sets the file path
        """
        ...
    
    def getFileSize(self) -> float:
        """
        Cython signature: float getFileSize()
        Returns the file size in MB
        """
        ...
    
    def setFileSize(self, in_0: float ) -> None:
        """
        Cython signature: void setFileSize(float)
        Sets the file size in MB
        """
        ...
    
    def getFileType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFileType()
        Returns the file type
        """
        ...
    
    def setFileType(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFileType(String)
        Sets the file type
        """
        ...
    
    def getChecksum(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getChecksum()
        Returns the file's checksum
        """
        ...
    
    def setChecksum(self, in_0: Union[bytes, str, String] , in_1: int ) -> None:
        """
        Cython signature: void setChecksum(String, ChecksumType)
        Sets the file's checksum
        """
        ...
    
    def getChecksumType(self) -> int:
        """
        Cython signature: ChecksumType getChecksumType()
        Returns the checksum type
        """
        ...
    
    def getNativeIDType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNativeIDType()
        Returns the native ID type of the spectra
        """
        ...
    
    def setNativeIDType(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNativeIDType(String)
        Sets the native ID type of the spectra
        """
        ...
    
    def getNativeIDTypeAccession(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNativeIDTypeAccession()
        Returns the nativeID of the spectra
        """
        ...
    
    def setNativeIDTypeAccession(self, accesssion: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNativeIDTypeAccession(const String & accesssion)
        Sets the native ID of the spectra
        """
        ... 


class TM_DataPoint:
    """
    Cython implementation of _TM_DataPoint

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TM_DataPoint.html>`_
    """
    
    first: float
    
    second: float
    
    note: Union[bytes, str, String]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TM_DataPoint()
        """
        ...
    
    @overload
    def __init__(self, in_0: float , in_1: float ) -> None:
        """
        Cython signature: void TM_DataPoint(double, double)
        """
        ...
    
    @overload
    def __init__(self, in_0: float , in_1: float , in_2: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void TM_DataPoint(double, double, const String &)
        """
        ...
    
    def __richcmp__(self, other: TM_DataPoint, op: int) -> Any:
        ... 


class TraceInfo:
    """
    Cython implementation of _TraceInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TraceInfo.html>`_
    """
    
    name: bytes
    
    description: bytes
    
    opened: bool
    
    @overload
    def __init__(self, n: Union[bytes, str] , d: Union[bytes, str] , o: bool ) -> None:
        """
        Cython signature: void TraceInfo(libcpp_utf8_string n, libcpp_utf8_string d, bool o)
        """
        ...
    
    @overload
    def __init__(self, in_0: TraceInfo ) -> None:
        """
        Cython signature: void TraceInfo(TraceInfo)
        """
        ... 


class TransformationModelBSpline:
    """
    Cython implementation of _TransformationModelBSpline

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TransformationModelBSpline.html>`_
      -- Inherits from ['TransformationModel']
    """
    
    def __init__(self, data: List[TM_DataPoint] , params: Param ) -> None:
        """
        Cython signature: void TransformationModelBSpline(libcpp_vector[TM_DataPoint] & data, Param & params)
        """
        ...
    
    def getDefaultParameters(self, in_0: Param ) -> None:
        """
        Cython signature: void getDefaultParameters(Param &)
        Gets the default parameters
        """
        ...
    
    def evaluate(self, value: float ) -> float:
        """
        Cython signature: double evaluate(double value)
        Evaluates the model at the given values
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        """
        ...
    
    def weightData(self, data: List[TM_DataPoint] ) -> None:
        """
        Cython signature: void weightData(libcpp_vector[TM_DataPoint] & data)
        Weight the data by the given weight function
        """
        ...
    
    def checkValidWeight(self, weight: Union[bytes, str, String] , valid_weights: List[bytes] ) -> bool:
        """
        Cython signature: bool checkValidWeight(const String & weight, libcpp_vector[String] & valid_weights)
        Check for a valid weighting function string
        """
        ...
    
    def weightDatum(self, datum: float , weight: Union[bytes, str, String] ) -> float:
        """
        Cython signature: double weightDatum(double & datum, const String & weight)
        Weight the data according to the weighting function
        """
        ...
    
    def unWeightDatum(self, datum: float , weight: Union[bytes, str, String] ) -> float:
        """
        Cython signature: double unWeightDatum(double & datum, const String & weight)
        Apply the reverse of the weighting function to the data
        """
        ...
    
    def getValidXWeights(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getValidXWeights()
        Returns a list of valid x weight function stringss
        """
        ...
    
    def getValidYWeights(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getValidYWeights()
        Returns a list of valid y weight function strings
        """
        ...
    
    def unWeightData(self, data: List[TM_DataPoint] ) -> None:
        """
        Cython signature: void unWeightData(libcpp_vector[TM_DataPoint] & data)
        Unweight the data by the given weight function
        """
        ...
    
    def checkDatumRange(self, datum: float , datum_min: float , datum_max: float ) -> float:
        """
        Cython signature: double checkDatumRange(const double & datum, const double & datum_min, const double & datum_max)
        Check that the datum is within the valid min and max bounds
        """
        ...
    
    getDefaultParameters: __static_TransformationModelBSpline_getDefaultParameters 


class TransformationModelInterpolated:
    """
    Cython implementation of _TransformationModelInterpolated

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TransformationModelInterpolated.html>`_
      -- Inherits from ['TransformationModel']
    """
    
    def __init__(self, data: List[TM_DataPoint] , params: Param ) -> None:
        """
        Cython signature: void TransformationModelInterpolated(libcpp_vector[TM_DataPoint] & data, Param & params)
        """
        ...
    
    def getDefaultParameters(self, in_0: Param ) -> None:
        """
        Cython signature: void getDefaultParameters(Param &)
        Gets the default parameters
        """
        ...
    
    def evaluate(self, value: float ) -> float:
        """
        Cython signature: double evaluate(double value)
        Evaluate the interpolation model at the given value
        
        :param value: The position where the interpolation should be evaluated
        :returns: The interpolated value
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        """
        ...
    
    def weightData(self, data: List[TM_DataPoint] ) -> None:
        """
        Cython signature: void weightData(libcpp_vector[TM_DataPoint] & data)
        Weight the data by the given weight function
        """
        ...
    
    def checkValidWeight(self, weight: Union[bytes, str, String] , valid_weights: List[bytes] ) -> bool:
        """
        Cython signature: bool checkValidWeight(const String & weight, libcpp_vector[String] & valid_weights)
        Check for a valid weighting function string
        """
        ...
    
    def weightDatum(self, datum: float , weight: Union[bytes, str, String] ) -> float:
        """
        Cython signature: double weightDatum(double & datum, const String & weight)
        Weight the data according to the weighting function
        """
        ...
    
    def unWeightDatum(self, datum: float , weight: Union[bytes, str, String] ) -> float:
        """
        Cython signature: double unWeightDatum(double & datum, const String & weight)
        Apply the reverse of the weighting function to the data
        """
        ...
    
    def getValidXWeights(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getValidXWeights()
        Returns a list of valid x weight function stringss
        """
        ...
    
    def getValidYWeights(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getValidYWeights()
        Returns a list of valid y weight function strings
        """
        ...
    
    def unWeightData(self, data: List[TM_DataPoint] ) -> None:
        """
        Cython signature: void unWeightData(libcpp_vector[TM_DataPoint] & data)
        Unweight the data by the given weight function
        """
        ...
    
    def checkDatumRange(self, datum: float , datum_min: float , datum_max: float ) -> float:
        """
        Cython signature: double checkDatumRange(const double & datum, const double & datum_min, const double & datum_max)
        Check that the datum is within the valid min and max bounds
        """
        ... 


class TransformationModelLowess:
    """
    Cython implementation of _TransformationModelLowess

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TransformationModelLowess.html>`_
      -- Inherits from ['TransformationModel']
    """
    
    def __init__(self, data: List[TM_DataPoint] , params: Param ) -> None:
        """
        Cython signature: void TransformationModelLowess(libcpp_vector[TM_DataPoint] & data, Param & params)
        """
        ...
    
    def getDefaultParameters(self, in_0: Param ) -> None:
        """
        Cython signature: void getDefaultParameters(Param &)
        """
        ...
    
    def evaluate(self, value: float ) -> float:
        """
        Cython signature: double evaluate(double value)
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        """
        ...
    
    def weightData(self, data: List[TM_DataPoint] ) -> None:
        """
        Cython signature: void weightData(libcpp_vector[TM_DataPoint] & data)
        Weight the data by the given weight function
        """
        ...
    
    def checkValidWeight(self, weight: Union[bytes, str, String] , valid_weights: List[bytes] ) -> bool:
        """
        Cython signature: bool checkValidWeight(const String & weight, libcpp_vector[String] & valid_weights)
        Check for a valid weighting function string
        """
        ...
    
    def weightDatum(self, datum: float , weight: Union[bytes, str, String] ) -> float:
        """
        Cython signature: double weightDatum(double & datum, const String & weight)
        Weight the data according to the weighting function
        """
        ...
    
    def unWeightDatum(self, datum: float , weight: Union[bytes, str, String] ) -> float:
        """
        Cython signature: double unWeightDatum(double & datum, const String & weight)
        Apply the reverse of the weighting function to the data
        """
        ...
    
    def getValidXWeights(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getValidXWeights()
        Returns a list of valid x weight function stringss
        """
        ...
    
    def getValidYWeights(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getValidYWeights()
        Returns a list of valid y weight function strings
        """
        ...
    
    def unWeightData(self, data: List[TM_DataPoint] ) -> None:
        """
        Cython signature: void unWeightData(libcpp_vector[TM_DataPoint] & data)
        Unweight the data by the given weight function
        """
        ...
    
    def checkDatumRange(self, datum: float , datum_min: float , datum_max: float ) -> float:
        """
        Cython signature: double checkDatumRange(const double & datum, const double & datum_min, const double & datum_max)
        Check that the datum is within the valid min and max bounds
        """
        ...
    
    getDefaultParameters: __static_TransformationModelLowess_getDefaultParameters 


class Unit:
    """
    Cython implementation of _Unit

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Unit.html>`_
    """
    
    accession: Union[bytes, str, String]
    
    name: Union[bytes, str, String]
    
    cv_ref: Union[bytes, str, String]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Unit()
        """
        ...
    
    @overload
    def __init__(self, in_0: Unit ) -> None:
        """
        Cython signature: void Unit(Unit)
        """
        ...
    
    @overload
    def __init__(self, p_accession: Union[bytes, str, String] , p_name: Union[bytes, str, String] , p_cv_ref: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void Unit(const String & p_accession, const String & p_name, const String & p_cv_ref)
        """
        ...
    
    def __richcmp__(self, other: Unit, op: int) -> Any:
        ... 


class VersionDetails:
    """
    Cython implementation of _VersionDetails

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1VersionDetails.html>`_
    """
    
    version_major: int
    
    version_minor: int
    
    version_patch: int
    
    pre_release_identifier: Union[bytes, str, String]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void VersionDetails()
        """
        ...
    
    @overload
    def __init__(self, in_0: VersionDetails ) -> None:
        """
        Cython signature: void VersionDetails(VersionDetails &)
        """
        ...
    
    def __richcmp__(self, other: VersionDetails, op: int) -> Any:
        ...
    
    create: __static_VersionDetails_create 


class VersionInfo:
    """
    Cython implementation of _VersionInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1VersionInfo.html>`_
    """
    
    getBranch: __static_VersionInfo_getBranch
    
    getRevision: __static_VersionInfo_getRevision
    
    getTime: __static_VersionInfo_getTime
    
    getVersion: __static_VersionInfo_getVersion
    
    getVersionStruct: __static_VersionInfo_getVersionStruct 


class XMLFile:
    """
    Cython implementation of _XMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1XMLFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void XMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: XMLFile ) -> None:
        """
        Cython signature: void XMLFile(XMLFile &)
        """
        ...
    
    @overload
    def __init__(self, schema_location: Union[bytes, str, String] , version: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void XMLFile(const String & schema_location, const String & version)
        """
        ...
    
    def getVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVersion()
        Return the version of the schema
        """
        ... 


class XTandemInfile:
    """
    Cython implementation of _XTandemInfile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1XTandemInfile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void XTandemInfile()
        """
        ...
    
    def setFragmentMassTolerance(self, tolerance: float ) -> None:
        """
        Cython signature: void setFragmentMassTolerance(double tolerance)
        """
        ...
    
    def getFragmentMassTolerance(self) -> float:
        """
        Cython signature: double getFragmentMassTolerance()
        """
        ...
    
    def setPrecursorMassTolerancePlus(self, tol: float ) -> None:
        """
        Cython signature: void setPrecursorMassTolerancePlus(double tol)
        """
        ...
    
    def getPrecursorMassTolerancePlus(self) -> float:
        """
        Cython signature: double getPrecursorMassTolerancePlus()
        """
        ...
    
    def setPrecursorMassToleranceMinus(self, tol: float ) -> None:
        """
        Cython signature: void setPrecursorMassToleranceMinus(double tol)
        """
        ...
    
    def getPrecursorMassToleranceMinus(self) -> float:
        """
        Cython signature: double getPrecursorMassToleranceMinus()
        """
        ...
    
    def setPrecursorErrorType(self, mono_isotopic: int ) -> None:
        """
        Cython signature: void setPrecursorErrorType(MassType mono_isotopic)
        """
        ...
    
    def getPrecursorErrorType(self) -> int:
        """
        Cython signature: MassType getPrecursorErrorType()
        """
        ...
    
    def setFragmentMassErrorUnit(self, unit: int ) -> None:
        """
        Cython signature: void setFragmentMassErrorUnit(ErrorUnit unit)
        """
        ...
    
    def getFragmentMassErrorUnit(self) -> int:
        """
        Cython signature: ErrorUnit getFragmentMassErrorUnit()
        """
        ...
    
    def setPrecursorMassErrorUnit(self, unit: int ) -> None:
        """
        Cython signature: void setPrecursorMassErrorUnit(ErrorUnit unit)
        """
        ...
    
    def getPrecursorMassErrorUnit(self) -> int:
        """
        Cython signature: ErrorUnit getPrecursorMassErrorUnit()
        """
        ...
    
    def setNumberOfThreads(self, threads: int ) -> None:
        """
        Cython signature: void setNumberOfThreads(unsigned int threads)
        """
        ...
    
    def getNumberOfThreads(self) -> int:
        """
        Cython signature: unsigned int getNumberOfThreads()
        """
        ...
    
    def setModifications(self, mods: ModificationDefinitionsSet ) -> None:
        """
        Cython signature: void setModifications(ModificationDefinitionsSet & mods)
        """
        ...
    
    def getModifications(self) -> ModificationDefinitionsSet:
        """
        Cython signature: ModificationDefinitionsSet getModifications()
        """
        ...
    
    def setOutputFilename(self, output: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setOutputFilename(const String & output)
        """
        ...
    
    def getOutputFilename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOutputFilename()
        """
        ...
    
    def setInputFilename(self, input_file: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setInputFilename(const String & input_file)
        """
        ...
    
    def getInputFilename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getInputFilename()
        """
        ...
    
    def setTaxonomyFilename(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTaxonomyFilename(const String & filename)
        """
        ...
    
    def getTaxonomyFilename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTaxonomyFilename()
        """
        ...
    
    def setDefaultParametersFilename(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setDefaultParametersFilename(const String & filename)
        """
        ...
    
    def getDefaultParametersFilename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getDefaultParametersFilename()
        """
        ...
    
    def setTaxon(self, taxon: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTaxon(const String & taxon)
        """
        ...
    
    def getTaxon(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTaxon()
        """
        ...
    
    def setMaxPrecursorCharge(self, max_charge: int ) -> None:
        """
        Cython signature: void setMaxPrecursorCharge(int max_charge)
        """
        ...
    
    def getMaxPrecursorCharge(self) -> int:
        """
        Cython signature: int getMaxPrecursorCharge()
        """
        ...
    
    def setNumberOfMissedCleavages(self, missed_cleavages: int ) -> None:
        """
        Cython signature: void setNumberOfMissedCleavages(unsigned int missed_cleavages)
        """
        ...
    
    def getNumberOfMissedCleavages(self) -> int:
        """
        Cython signature: unsigned int getNumberOfMissedCleavages()
        """
        ...
    
    def setOutputResults(self, result: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setOutputResults(String result)
        """
        ...
    
    def getOutputResults(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOutputResults()
        """
        ...
    
    def setMaxValidEValue(self, value: float ) -> None:
        """
        Cython signature: void setMaxValidEValue(double value)
        """
        ...
    
    def getMaxValidEValue(self) -> float:
        """
        Cython signature: double getMaxValidEValue()
        """
        ...
    
    def setSemiCleavage(self, semi_cleavage: bool ) -> None:
        """
        Cython signature: void setSemiCleavage(bool semi_cleavage)
        """
        ...
    
    def setAllowIsotopeError(self, allow_isotope_error: bool ) -> None:
        """
        Cython signature: void setAllowIsotopeError(bool allow_isotope_error)
        """
        ...
    
    def write(self, filename: Union[bytes, str, String] , ignore_member_parameters: bool , force_default_mods: bool ) -> None:
        """
        Cython signature: void write(String filename, bool ignore_member_parameters, bool force_default_mods)
        """
        ...
    
    def setCleavageSite(self, cleavage_site: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCleavageSite(String cleavage_site)
        """
        ...
    
    def getCleavageSite(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCleavageSite()
        """
        ...
    ErrorUnit : __ErrorUnit
    MassType : __MassType 


class ChecksumType:
    None
    UNKNOWN_CHECKSUM : int
    SHA1 : int
    MD5 : int
    SIZE_OF_CHECKSUMTYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __ErrorUnit:
    None
    DALTONS : int
    PPM : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __IntensityThresholdCalculation:
    None
    MANUAL : int
    AUTOMAXBYSTDEV : int
    AUTOMAXBYPERCENT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __MassType:
    None
    MONOISOTOPIC : int
    AVERAGE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __OpenPepXLLFAlgorithm_ExitCodes:
    None
    EXECUTION_OK : int
    ILLEGAL_PARAMETERS : int
    UNEXPECTED_RESULT : int
    INCOMPATIBLE_INPUT_DATA : int

    def getMapping(self) -> Dict[int, str]:
       ... 

