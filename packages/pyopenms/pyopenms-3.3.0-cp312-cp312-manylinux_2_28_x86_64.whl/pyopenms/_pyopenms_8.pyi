from __future__ import annotations
from typing import overload, Any, List, Dict, Tuple, Set, Sequence, Union
from pyopenms import *  # pylint: disable=wildcard-import; lgtm(py/polluting-import)
import numpy as _np

from enum import Enum as _PyEnum


def __static_File_absolutePath(file: Union[bytes, str, String] ) -> Union[bytes, str, String]:
    """
    Cython signature: String absolutePath(String file)
    """
    ...

def __static_File_basename(file: Union[bytes, str, String] ) -> Union[bytes, str, String]:
    """
    Cython signature: String basename(String file)
    """
    ...

def __static_MetaboliteSpectralMatching_computeHyperScore(fragment_mass_error: float , fragment_mass_tolerance_unit_ppm: bool , exp_spectrum: MSSpectrum , db_spectrum: MSSpectrum , annotations: List[PeptideHit_PeakAnnotation] , mz_lower_bound: float ) -> float:
    """
    Cython signature: double computeHyperScore(double fragment_mass_error, bool fragment_mass_tolerance_unit_ppm, MSSpectrum exp_spectrum, MSSpectrum db_spectrum, libcpp_vector[PeptideHit_PeakAnnotation] & annotations, double mz_lower_bound)
    """
    ...

def __static_Deisotoper_deisotopeAndSingleCharge(spectra: MSSpectrum , fragment_tolerance: float , fragment_unit_ppm: bool , min_charge: int , max_charge: int , keep_only_deisotoped: bool , min_isopeaks: int , max_isopeaks: int , make_single_charged: bool , annotate_charge: bool , annotate_iso_peak_count: bool , use_decreasing_model: bool , start_intensity_check: int , add_up_intensity: bool , annotate_features: bool ) -> None:
    """
    Cython signature: void deisotopeAndSingleCharge(MSSpectrum & spectra, double fragment_tolerance, bool fragment_unit_ppm, int min_charge, int max_charge, bool keep_only_deisotoped, unsigned int min_isopeaks, unsigned int max_isopeaks, bool make_single_charged, bool annotate_charge, bool annotate_iso_peak_count, bool use_decreasing_model, unsigned int start_intensity_check, bool add_up_intensity, bool annotate_features)
    """
    ...

def __static_Deisotoper_deisotopeAndSingleChargeDefault(spectra: MSSpectrum , fragment_tolerance: float , fragment_unit_ppm: bool ) -> None:
    """
    Cython signature: void deisotopeAndSingleChargeDefault(MSSpectrum & spectra, double fragment_tolerance, bool fragment_unit_ppm)
    """
    ...

def __static_Deisotoper_deisotopeWithAveragineModel(spectrum: MSSpectrum , fragment_tolerance: float , fragment_unit_ppm: bool , number_of_final_peaks: int , min_charge: int , max_charge: int , keep_only_deisotoped: bool , min_isopeaks: int , max_isopeaks: int , make_single_charged: bool , annotate_charge: bool , annotate_iso_peak_count: bool , add_up_intensity: bool ) -> None:
    """
    Cython signature: void deisotopeWithAveragineModel(MSSpectrum & spectrum, double fragment_tolerance, bool fragment_unit_ppm, int number_of_final_peaks, int min_charge, int max_charge, bool keep_only_deisotoped, unsigned int min_isopeaks, unsigned int max_isopeaks, bool make_single_charged, bool annotate_charge, bool annotate_iso_peak_count, bool add_up_intensity)
    """
    ...

def __static_File_empty(file_: Union[bytes, str, String] ) -> bool:
    """
    Cython signature: bool empty(String file_)
    """
    ...

def __static_File_exists(file_: Union[bytes, str, String] ) -> bool:
    """
    Cython signature: bool exists(String file_)
    """
    ...

def __static_File_fileList(dir: Union[bytes, str, String] , file_pattern: Union[bytes, str, String] , output: List[bytes] , full_path: bool ) -> bool:
    """
    Cython signature: bool fileList(String dir, String file_pattern, StringList output, bool full_path)
    """
    ...

def __static_File_find(filename: Union[bytes, str, String] , directories: List[bytes] ) -> Union[bytes, str, String]:
    """
    Cython signature: String find(String filename, StringList directories)
    """
    ...

def __static_File_findDatabase(db_name: Union[bytes, str, String] ) -> Union[bytes, str, String]:
    """
    Cython signature: String findDatabase(String db_name)
    """
    ...

def __static_File_findDoc(filename: Union[bytes, str, String] ) -> Union[bytes, str, String]:
    """
    Cython signature: String findDoc(String filename)
    """
    ...

def __static_File_findExecutable(toolName: Union[bytes, str, String] ) -> Union[bytes, str, String]:
    """
    Cython signature: String findExecutable(String toolName)
    """
    ...

def __static_File_getExecutablePath() -> Union[bytes, str, String]:
    """
    Cython signature: String getExecutablePath()
    """
    ...

def __static_File_getOpenMSDataPath() -> Union[bytes, str, String]:
    """
    Cython signature: String getOpenMSDataPath()
    """
    ...

def __static_File_getOpenMSHomePath() -> Union[bytes, str, String]:
    """
    Cython signature: String getOpenMSHomePath()
    """
    ...

def __static_File_getSystemParameters() -> Param:
    """
    Cython signature: Param getSystemParameters()
    """
    ...

def __static_File_getTempDirectory() -> Union[bytes, str, String]:
    """
    Cython signature: String getTempDirectory()
    """
    ...

def __static_File_getTemporaryFile(alternative_file: Union[bytes, str, String] ) -> Union[bytes, str, String]:
    """
    Cython signature: String getTemporaryFile(const String & alternative_file)
    """
    ...

def __static_File_getUniqueName() -> Union[bytes, str, String]:
    """
    Cython signature: String getUniqueName()
    """
    ...

def __static_File_getUserDirectory() -> Union[bytes, str, String]:
    """
    Cython signature: String getUserDirectory()
    """
    ...

def __static_File_isDirectory(path: Union[bytes, str, String] ) -> bool:
    """
    Cython signature: bool isDirectory(String path)
    """
    ...

def __static_DateTime_now() -> DateTime:
    """
    Cython signature: DateTime now()
    """
    ...

def __static_File_path(file: Union[bytes, str, String] ) -> Union[bytes, str, String]:
    """
    Cython signature: String path(String file)
    """
    ...

def __static_File_readable(file: Union[bytes, str, String] ) -> bool:
    """
    Cython signature: bool readable(String file)
    """
    ...

def __static_File_remove(file_: Union[bytes, str, String] ) -> bool:
    """
    Cython signature: bool remove(String file_)
    """
    ...

def __static_File_removeDirRecursively(dir_name: Union[bytes, str, String] ) -> bool:
    """
    Cython signature: bool removeDirRecursively(String dir_name)
    """
    ...

def __static_File_rename(from_: Union[bytes, str, String] , to: Union[bytes, str, String] , overwrite_existing: bool , verbose: bool ) -> bool:
    """
    Cython signature: bool rename(const String & from_, const String & to, bool overwrite_existing, bool verbose)
    """
    ...

def __static_IMTypes_toDriftTimeUnit(dtu_string: bytes ) -> int:
    """
    Cython signature: DriftTimeUnit toDriftTimeUnit(const libcpp_string & dtu_string)
    """
    ...

def __static_IMTypes_toIMFormat(IM_format: bytes ) -> int:
    """
    Cython signature: IMFormat toIMFormat(const libcpp_string & IM_format)
    """
    ...

def __static_IMTypes_toString(value: int ) -> bytes:
    """
    Cython signature: libcpp_string toString(const DriftTimeUnit value)
    """
    ...

def __static_IMTypes_toString(value: int ) -> bytes:
    """
    Cython signature: libcpp_string toString(const IMFormat value)
    """
    ...

def __static_File_writable(file: Union[bytes, str, String] ) -> bool:
    """
    Cython signature: bool writable(String file)
    """
    ...


class AQS_featureConcentration:
    """
    Cython implementation of _AQS_featureConcentration

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AQS_featureConcentration.html>`_
    """
    
    feature: Feature
    
    IS_feature: Feature
    
    actual_concentration: float
    
    IS_actual_concentration: float
    
    concentration_units: Union[bytes, str, String]
    
    dilution_factor: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AQS_featureConcentration()
        """
        ...
    
    @overload
    def __init__(self, in_0: AQS_featureConcentration ) -> None:
        """
        Cython signature: void AQS_featureConcentration(AQS_featureConcentration &)
        """
        ... 


class AQS_runConcentration:
    """
    Cython implementation of _AQS_runConcentration

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AQS_runConcentration.html>`_
    """
    
    sample_name: Union[bytes, str, String]
    
    component_name: Union[bytes, str, String]
    
    IS_component_name: Union[bytes, str, String]
    
    actual_concentration: float
    
    IS_actual_concentration: float
    
    concentration_units: Union[bytes, str, String]
    
    dilution_factor: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AQS_runConcentration()
        """
        ...
    
    @overload
    def __init__(self, in_0: AQS_runConcentration ) -> None:
        """
        Cython signature: void AQS_runConcentration(AQS_runConcentration &)
        """
        ... 


class AbsoluteQuantitationStandards:
    """
    Cython implementation of _AbsoluteQuantitationStandards

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AbsoluteQuantitationStandards.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AbsoluteQuantitationStandards()
        """
        ...
    
    @overload
    def __init__(self, in_0: AbsoluteQuantitationStandards ) -> None:
        """
        Cython signature: void AbsoluteQuantitationStandards(AbsoluteQuantitationStandards &)
        """
        ...
    
    def getComponentFeatureConcentrations(self, run_concentrations: List[AQS_runConcentration] , feature_maps: List[FeatureMap] , component_name: Union[bytes, str, String] , feature_concentrations: List[AQS_featureConcentration] ) -> None:
        """
        Cython signature: void getComponentFeatureConcentrations(libcpp_vector[AQS_runConcentration] & run_concentrations, libcpp_vector[FeatureMap] & feature_maps, const String & component_name, libcpp_vector[AQS_featureConcentration] & feature_concentrations)
        """
        ... 


class AverageLinkage:
    """
    Cython implementation of _AverageLinkage

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AverageLinkage.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AverageLinkage()
        """
        ...
    
    @overload
    def __init__(self, in_0: AverageLinkage ) -> None:
        """
        Cython signature: void AverageLinkage(AverageLinkage &)
        """
        ... 


class BilinearInterpolation:
    """
    Cython implementation of _BilinearInterpolation[double,double]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1BilinearInterpolation[double,double].html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void BilinearInterpolation()
        """
        ...
    
    @overload
    def __init__(self, in_0: BilinearInterpolation ) -> None:
        """
        Cython signature: void BilinearInterpolation(BilinearInterpolation &)
        """
        ...
    
    def value(self, arg_pos_0: float , arg_pos_1: float ) -> float:
        """
        Cython signature: double value(double arg_pos_0, double arg_pos_1)
        """
        ...
    
    def addValue(self, arg_pos_0: float , arg_pos_1: float , arg_value: float ) -> None:
        """
        Cython signature: void addValue(double arg_pos_0, double arg_pos_1, double arg_value)
        Performs bilinear resampling. The arg_value is split up and added to the data points around arg_pos. ("forward resampling")
        """
        ...
    
    def getData(self) -> MatrixDouble:
        """
        Cython signature: MatrixDouble getData()
        """
        ...
    
    def setData(self, data: MatrixDouble ) -> None:
        """
        Cython signature: void setData(MatrixDouble & data)
        Assigns data to the internal random access container storing the data. SourceContainer must be assignable to ContainerType
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        """
        ...
    
    def key2index_0(self, pos: float ) -> float:
        """
        Cython signature: double key2index_0(double pos)
        The transformation from "outside" to "inside" coordinates
        """
        ...
    
    def index2key_0(self, pos: float ) -> float:
        """
        Cython signature: double index2key_0(double pos)
        The transformation from "inside" to "outside" coordinates
        """
        ...
    
    def key2index_1(self, pos: float ) -> float:
        """
        Cython signature: double key2index_1(double pos)
        The transformation from "outside" to "inside" coordinates
        """
        ...
    
    def index2key_1(self, pos: float ) -> float:
        """
        Cython signature: double index2key_1(double pos)
        The transformation from "inside" to "outside" coordinates
        """
        ...
    
    def getScale_0(self) -> float:
        """
        Cython signature: double getScale_0()
        """
        ...
    
    def setScale_0(self, scale: float ) -> None:
        """
        Cython signature: void setScale_0(double & scale)
        """
        ...
    
    def getScale_1(self) -> float:
        """
        Cython signature: double getScale_1()
        """
        ...
    
    def setScale_1(self, scale: float ) -> None:
        """
        Cython signature: void setScale_1(double & scale)
        """
        ...
    
    def getOffset_0(self) -> float:
        """
        Cython signature: double getOffset_0()
        Accessor. "Offset" is the point (in "outside" units) which corresponds to "Data(0,0)"
        """
        ...
    
    def setOffset_0(self, offset: float ) -> None:
        """
        Cython signature: void setOffset_0(double & offset)
        """
        ...
    
    def getOffset_1(self) -> float:
        """
        Cython signature: double getOffset_1()
        Accessor. "Offset" is the point (in "outside" units) which corresponds to "Data(0,0)"
        """
        ...
    
    def setOffset_1(self, offset: float ) -> None:
        """
        Cython signature: void setOffset_1(double & offset)
        """
        ...
    
    @overload
    def setMapping_0(self, scale: float , inside: float , outside: float ) -> None:
        """
        Cython signature: void setMapping_0(double & scale, double & inside, double & outside)
        """
        ...
    
    @overload
    def setMapping_0(self, inside_low: float , outside_low: float , inside_high: float , outside_high: float ) -> None:
        """
        Cython signature: void setMapping_0(double & inside_low, double & outside_low, double & inside_high, double & outside_high)
        """
        ...
    
    @overload
    def setMapping_1(self, scale: float , inside: float , outside: float ) -> None:
        """
        Cython signature: void setMapping_1(double & scale, double & inside, double & outside)
        """
        ...
    
    @overload
    def setMapping_1(self, inside_low: float , outside_low: float , inside_high: float , outside_high: float ) -> None:
        """
        Cython signature: void setMapping_1(double & inside_low, double & outside_low, double & inside_high, double & outside_high)
        """
        ...
    
    def getInsideReferencePoint_0(self) -> float:
        """
        Cython signature: double getInsideReferencePoint_0()
        """
        ...
    
    def getInsideReferencePoint_1(self) -> float:
        """
        Cython signature: double getInsideReferencePoint_1()
        """
        ...
    
    def getOutsideReferencePoint_0(self) -> float:
        """
        Cython signature: double getOutsideReferencePoint_0()
        """
        ...
    
    def getOutsideReferencePoint_1(self) -> float:
        """
        Cython signature: double getOutsideReferencePoint_1()
        """
        ...
    
    def supportMin_0(self) -> float:
        """
        Cython signature: double supportMin_0()
        Lower boundary of the support, in "outside" coordinates
        """
        ...
    
    def supportMin_1(self) -> float:
        """
        Cython signature: double supportMin_1()
        Lower boundary of the support, in "outside" coordinates
        """
        ...
    
    def supportMax_0(self) -> float:
        """
        Cython signature: double supportMax_0()
        Upper boundary of the support, in "outside" coordinates
        """
        ...
    
    def supportMax_1(self) -> float:
        """
        Cython signature: double supportMax_1()
        Upper boundary of the support, in "outside" coordinates
        """
        ... 


class CVTermListInterface:
    """
    Cython implementation of _CVTermListInterface

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVTermListInterface.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVTermListInterface()
        """
        ...
    
    @overload
    def __init__(self, in_0: CVTermListInterface ) -> None:
        """
        Cython signature: void CVTermListInterface(CVTermListInterface &)
        """
        ...
    
    @overload
    def replaceCVTerms(self, cv_terms: Dict[bytes,List[CVTerm]] ) -> None:
        """
        Cython signature: void replaceCVTerms(libcpp_map[String,libcpp_vector[CVTerm]] & cv_terms)
        """
        ...
    
    @overload
    def replaceCVTerms(self, cv_terms: List[CVTerm] , accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void replaceCVTerms(libcpp_vector[CVTerm] & cv_terms, const String & accession)
        """
        ...
    
    def setCVTerms(self, terms: List[CVTerm] ) -> None:
        """
        Cython signature: void setCVTerms(libcpp_vector[CVTerm] & terms)
        """
        ...
    
    def replaceCVTerm(self, cv_term: CVTerm ) -> None:
        """
        Cython signature: void replaceCVTerm(CVTerm & cv_term)
        """
        ...
    
    def consumeCVTerms(self, cv_term_map: Dict[bytes,List[CVTerm]] ) -> None:
        """
        Cython signature: void consumeCVTerms(libcpp_map[String,libcpp_vector[CVTerm]] & cv_term_map)
        Merges the given map into the member map, no duplicate checking
        """
        ...
    
    def getCVTerms(self) -> Dict[bytes,List[CVTerm]]:
        """
        Cython signature: libcpp_map[String,libcpp_vector[CVTerm]] getCVTerms()
        """
        ...
    
    def addCVTerm(self, term: CVTerm ) -> None:
        """
        Cython signature: void addCVTerm(CVTerm & term)
        Adds a CV term
        """
        ...
    
    def hasCVTerm(self, accession: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasCVTerm(const String & accession)
        Checks whether the term has a value
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
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
    
    def __richcmp__(self, other: CVTermListInterface, op: int) -> Any:
        ... 


class CachedSwathFileConsumer:
    """
    Cython implementation of _CachedSwathFileConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CachedSwathFileConsumer.html>`_
      -- Inherits from ['FullSwathFileConsumer']
    """
    
    @overload
    def __init__(self, in_0: CachedSwathFileConsumer ) -> None:
        """
        Cython signature: void CachedSwathFileConsumer(CachedSwathFileConsumer &)
        """
        ...
    
    @overload
    def __init__(self, cachedir: Union[bytes, str, String] , basename: Union[bytes, str, String] , nr_ms1_spectra: int , nr_ms2_spectra: List[int] ) -> None:
        """
        Cython signature: void CachedSwathFileConsumer(String cachedir, String basename, size_t nr_ms1_spectra, libcpp_vector[int] nr_ms2_spectra)
        """
        ...
    
    def setExpectedSize(self, s: int , c: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t s, size_t c)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings exp)
        """
        ...
    
    def retrieveSwathMaps(self, maps: List[SwathMap] ) -> None:
        """
        Cython signature: void retrieveSwathMaps(libcpp_vector[SwathMap] & maps)
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
        """
        ... 


class ChannelInfo:
    """
    Cython implementation of _ChannelInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ChannelInfo.html>`_
    """
    
    description: bytes
    
    name: int
    
    id: int
    
    center: float
    
    active: bool 


class ClusterProxyKD:
    """
    Cython implementation of _ClusterProxyKD

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ClusterProxyKD.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ClusterProxyKD()
        """
        ...
    
    @overload
    def __init__(self, in_0: ClusterProxyKD ) -> None:
        """
        Cython signature: void ClusterProxyKD(ClusterProxyKD &)
        """
        ...
    
    @overload
    def __init__(self, size: int , avg_distance: float , center_index: int ) -> None:
        """
        Cython signature: void ClusterProxyKD(size_t size, double avg_distance, size_t center_index)
        """
        ...
    
    def getSize(self) -> int:
        """
        Cython signature: size_t getSize()
        """
        ...
    
    def isValid(self) -> bool:
        """
        Cython signature: bool isValid()
        """
        ...
    
    def getAvgDistance(self) -> float:
        """
        Cython signature: double getAvgDistance()
        """
        ...
    
    def getCenterIndex(self) -> int:
        """
        Cython signature: size_t getCenterIndex()
        """
        ...
    
    def __richcmp__(self, other: ClusterProxyKD, op: int) -> Any:
        ... 


class ConsensusMapNormalizerAlgorithmMedian:
    """
    Cython implementation of _ConsensusMapNormalizerAlgorithmMedian

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ConsensusMapNormalizerAlgorithmMedian_1_1ConsensusMapNormalizerAlgorithmMedian.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusMapNormalizerAlgorithmMedian()
        """
        ...
    
    def computeMedians(self, input_map: ConsensusMap , medians: List[float] , acc_filter: Union[bytes, str, String] , desc_filter: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t computeMedians(ConsensusMap & input_map, libcpp_vector[double] & medians, const String & acc_filter, const String & desc_filter)
        Computes medians of all maps and returns index of map with most features
        """
        ...
    
    def normalizeMaps(self, input_map: ConsensusMap , method: int , acc_filter: Union[bytes, str, String] , desc_filter: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void normalizeMaps(ConsensusMap & input_map, NormalizationMethod method, const String & acc_filter, const String & desc_filter)
        Normalizes the maps of the consensusMap
        """
        ... 


class CrossLinkSpectrumMatch:
    """
    Cython implementation of _CrossLinkSpectrumMatch

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::OPXLDataStructs_1_1CrossLinkSpectrumMatch.html>`_
    """
    
    cross_link: ProteinProteinCrossLink
    
    scan_index_light: int
    
    scan_index_heavy: int
    
    score: float
    
    rank: int
    
    xquest_score: float
    
    pre_score: float
    
    percTIC: float
    
    wTIC: float
    
    wTICold: float
    
    int_sum: float
    
    intsum_alpha: float
    
    intsum_beta: float
    
    total_current: float
    
    precursor_error_ppm: float
    
    match_odds: float
    
    match_odds_alpha: float
    
    match_odds_beta: float
    
    log_occupancy: float
    
    log_occupancy_alpha: float
    
    log_occupancy_beta: float
    
    xcorrx_max: float
    
    xcorrc_max: float
    
    matched_linear_alpha: int
    
    matched_linear_beta: int
    
    matched_xlink_alpha: int
    
    matched_xlink_beta: int
    
    num_iso_peaks_mean: float
    
    num_iso_peaks_mean_linear_alpha: float
    
    num_iso_peaks_mean_linear_beta: float
    
    num_iso_peaks_mean_xlinks_alpha: float
    
    num_iso_peaks_mean_xlinks_beta: float
    
    ppm_error_abs_sum_linear_alpha: float
    
    ppm_error_abs_sum_linear_beta: float
    
    ppm_error_abs_sum_xlinks_alpha: float
    
    ppm_error_abs_sum_xlinks_beta: float
    
    ppm_error_abs_sum_linear: float
    
    ppm_error_abs_sum_xlinks: float
    
    ppm_error_abs_sum_alpha: float
    
    ppm_error_abs_sum_beta: float
    
    ppm_error_abs_sum: float
    
    precursor_correction: int
    
    precursor_total_intensity: float
    
    precursor_target_intensity: float
    
    precursor_signal_proportion: float
    
    precursor_target_peak_count: int
    
    precursor_residual_peak_count: int
    
    frag_annotations: List[PeptideHit_PeakAnnotation]
    
    peptide_id_index: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CrossLinkSpectrumMatch()
        """
        ...
    
    @overload
    def __init__(self, in_0: CrossLinkSpectrumMatch ) -> None:
        """
        Cython signature: void CrossLinkSpectrumMatch(CrossLinkSpectrumMatch &)
        """
        ... 


class DBoundingBox2:
    """
    Cython implementation of _DBoundingBox2

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DBoundingBox2.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DBoundingBox2()
        """
        ...
    
    @overload
    def __init__(self, in_0: DBoundingBox2 ) -> None:
        """
        Cython signature: void DBoundingBox2(DBoundingBox2 &)
        """
        ...
    
    def minPosition(self) -> Union[Sequence[int], Sequence[float]]:
        """
        Cython signature: DPosition2 minPosition()
        """
        ...
    
    def maxPosition(self) -> Union[Sequence[int], Sequence[float]]:
        """
        Cython signature: DPosition2 maxPosition()
        """
        ... 


class DIAScoring:
    """
    Cython implementation of _DIAScoring

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DIAScoring.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void DIAScoring()
        """
        ...
    
    def dia_ms1_massdiff_score(self, precursor_mz: float , spectrum: List[OSSpectrum] , im_range: RangeMobility , ppm_score: float ) -> bool:
        """
        Cython signature: bool dia_ms1_massdiff_score(double precursor_mz, libcpp_vector[shared_ptr[OSSpectrum]] spectrum, RangeMobility & im_range, double & ppm_score)
        """
        ...
    
    def dia_ms1_isotope_scores_averagine(self, precursor_mz: float , spectrum: List[OSSpectrum] , charge_state: int , im_range: RangeMobility , isotope_corr: float , isotope_overlap: float ) -> None:
        """
        Cython signature: void dia_ms1_isotope_scores_averagine(double precursor_mz, libcpp_vector[shared_ptr[OSSpectrum]] spectrum, int charge_state, RangeMobility & im_range, double & isotope_corr, double & isotope_overlap)
        """
        ...
    
    def dia_ms1_isotope_scores(self, precursor_mz: float , spectrum: List[OSSpectrum] , im_range: RangeMobility , isotope_corr: float , isotope_overlap: float , sum_formula: EmpiricalFormula ) -> None:
        """
        Cython signature: void dia_ms1_isotope_scores(double precursor_mz, libcpp_vector[shared_ptr[OSSpectrum]] spectrum, RangeMobility & im_range, double & isotope_corr, double & isotope_overlap, EmpiricalFormula & sum_formula)
        """
        ...
    
    def score_with_isotopes(self, spectrum: List[OSSpectrum] , transitions: List[LightTransition] , im_range: RangeMobility , dotprod: float , manhattan: float ) -> None:
        """
        Cython signature: void score_with_isotopes(libcpp_vector[shared_ptr[OSSpectrum]] spectrum, libcpp_vector[LightTransition] transitions, RangeMobility & im_range, double & dotprod, double & manhattan)
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


class DateTime:
    """
    Cython implementation of _DateTime

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DateTime.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DateTime()
        """
        ...
    
    @overload
    def __init__(self, in_0: DateTime ) -> None:
        """
        Cython signature: void DateTime(DateTime &)
        """
        ...
    
    def setDate(self, date: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setDate(String date)
        """
        ...
    
    def setTime(self, date: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTime(String date)
        """
        ...
    
    def getDate(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getDate()
        """
        ...
    
    def getTime(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTime()
        """
        ...
    
    def now(self) -> DateTime:
        """
        Cython signature: DateTime now()
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ...
    
    def get(self) -> Union[bytes, str, String]:
        """
        Cython signature: String get()
        """
        ...
    
    def set(self, date: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void set(String date)
        """
        ...
    
    now: __static_DateTime_now 


class Deisotoper:
    """
    Cython implementation of _Deisotoper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Deisotoper.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Deisotoper()
        """
        ...
    
    @overload
    def __init__(self, in_0: Deisotoper ) -> None:
        """
        Cython signature: void Deisotoper(Deisotoper &)
        """
        ...
    
    deisotopeAndSingleCharge: __static_Deisotoper_deisotopeAndSingleCharge
    
    deisotopeAndSingleChargeDefault: __static_Deisotoper_deisotopeAndSingleChargeDefault
    
    deisotopeWithAveragineModel: __static_Deisotoper_deisotopeWithAveragineModel 


class DigestionEnzymeProtein:
    """
    Cython implementation of _DigestionEnzymeProtein

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DigestionEnzymeProtein.html>`_
      -- Inherits from ['DigestionEnzyme']

    Representation of a digestion enzyme for proteins (protease)
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DigestionEnzymeProtein()
        """
        ...
    
    @overload
    def __init__(self, in_0: DigestionEnzymeProtein ) -> None:
        """
        Cython signature: void DigestionEnzymeProtein(DigestionEnzymeProtein &)
        """
        ...
    
    @overload
    def __init__(self, name: Union[bytes, str, String] , cleavage_regex: Union[bytes, str, String] , synonyms: Set[bytes] , regex_description: Union[bytes, str, String] , n_term_gain: EmpiricalFormula , c_term_gain: EmpiricalFormula , psi_id: Union[bytes, str, String] , xtandem_id: Union[bytes, str, String] , comet_id: int , omssa_id: int ) -> None:
        """
        Cython signature: void DigestionEnzymeProtein(String name, String cleavage_regex, libcpp_set[String] synonyms, String regex_description, EmpiricalFormula n_term_gain, EmpiricalFormula c_term_gain, String psi_id, String xtandem_id, unsigned int comet_id, unsigned int omssa_id)
        """
        ...
    
    def setNTermGain(self, value: EmpiricalFormula ) -> None:
        """
        Cython signature: void setNTermGain(EmpiricalFormula value)
        Sets the N-term gain
        """
        ...
    
    def setCTermGain(self, value: EmpiricalFormula ) -> None:
        """
        Cython signature: void setCTermGain(EmpiricalFormula value)
        Sets the C-term gain
        """
        ...
    
    def getNTermGain(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getNTermGain()
        Returns the N-term gain
        """
        ...
    
    def getCTermGain(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getCTermGain()
        Returns the C-term gain
        """
        ...
    
    def setPSIID(self, value: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setPSIID(String value)
        Sets the PSI ID
        """
        ...
    
    def getPSIID(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getPSIID()
        Returns the PSI ID
        """
        ...
    
    def setXTandemID(self, value: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setXTandemID(String value)
        Sets the X! Tandem enzyme ID
        """
        ...
    
    def getXTandemID(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getXTandemID()
        Returns the X! Tandem enzyme ID
        """
        ...
    
    def setCometID(self, value: int ) -> None:
        """
        Cython signature: void setCometID(int value)
        Sets the Comet enzyme ID
        """
        ...
    
    def getCometID(self) -> int:
        """
        Cython signature: int getCometID()
        Returns the Comet enzyme ID
        """
        ...
    
    def setOMSSAID(self, value: int ) -> None:
        """
        Cython signature: void setOMSSAID(int value)
        Sets the OMSSA enzyme ID
        """
        ...
    
    def getOMSSAID(self) -> int:
        """
        Cython signature: int getOMSSAID()
        Returns the OMSSA enzyme ID
        """
        ...
    
    def setMSGFID(self, value: int ) -> None:
        """
        Cython signature: void setMSGFID(int value)
        Sets the MSGFPlus enzyme id
        """
        ...
    
    def getMSGFID(self) -> int:
        """
        Cython signature: int getMSGFID()
        Returns the MSGFPlus enzyme id
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String & name)
        Sets the name of the enzyme
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the enzyme
        """
        ...
    
    def setSynonyms(self, synonyms: Set[bytes] ) -> None:
        """
        Cython signature: void setSynonyms(libcpp_set[String] & synonyms)
        Sets the synonyms
        """
        ...
    
    def addSynonym(self, synonym: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addSynonym(const String & synonym)
        Adds a synonym
        """
        ...
    
    def getSynonyms(self) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getSynonyms()
        Returns the synonyms
        """
        ...
    
    def setRegEx(self, cleavage_regex: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setRegEx(const String & cleavage_regex)
        Sets the cleavage regex
        """
        ...
    
    def getRegEx(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getRegEx()
        Returns the cleavage regex
        """
        ...
    
    def setRegExDescription(self, value: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setRegExDescription(const String & value)
        Sets the regex description
        """
        ...
    
    def getRegExDescription(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getRegExDescription()
        Returns the regex description
        """
        ...
    
    def setValueFromFile(self, key: Union[bytes, str, String] , value: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool setValueFromFile(String key, String value)
        Sets the value of a member variable based on an entry from an input file
        """
        ...
    
    def __richcmp__(self, other: DigestionEnzymeProtein, op: int) -> Any:
        ... 


class FeatureMap:
    """
    Cython implementation of _FeatureMap

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureMap.html>`_
      -- Inherits from ['UniqueIdInterface', 'DocumentIdentifier', 'RangeManagerRtMzInt', 'MetaInfoInterface']

    A container for features.
    
    A feature map is a container holding features, which represent
    chemical entities (peptides, proteins, small molecules etc.) found
    in an LC-MS/MS experiment.
    
    This class supports direct iteration in Python.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureMap()
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureMap ) -> None:
        """
        Cython signature: void FeatureMap(FeatureMap &)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: int size()
        """
        ...
    
    def __getitem__(self, in_0: int ) -> Feature:
        """
        Cython signature: Feature & operator[](size_t)
        """
        ...
    def __setitem__(self, key: int, value: Feature ) -> None:
        """Cython signature: Feature & operator[](size_t)"""
        ...
    
    @overload
    def push_back(self, spec: Feature ) -> None:
        """
        Cython signature: void push_back(Feature spec)
        """
        ...
    
    @overload
    def push_back(self, spec: MRMFeature ) -> None:
        """
        Cython signature: void push_back(MRMFeature spec)
        """
        ...
    
    @overload
    def sortByIntensity(self, ) -> None:
        """
        Cython signature: void sortByIntensity()
        Sorts the peaks according to ascending intensity
        """
        ...
    
    @overload
    def sortByIntensity(self, reverse: bool ) -> None:
        """
        Cython signature: void sortByIntensity(bool reverse)
        Sorts the peaks according to ascending intensity. Order is reversed if argument is `true` ( reverse = true )
        """
        ...
    
    def sortByPosition(self) -> None:
        """
        Cython signature: void sortByPosition()
        Sorts features by position. Lexicographical comparison (first RT then m/z) is done
        """
        ...
    
    def sortByRT(self) -> None:
        """
        Cython signature: void sortByRT()
        Sorts features by RT position
        """
        ...
    
    def sortByMZ(self) -> None:
        """
        Cython signature: void sortByMZ()
        Sorts features by m/z position
        """
        ...
    
    def sortByOverallQuality(self) -> None:
        """
        Cython signature: void sortByOverallQuality()
        Sorts features by ascending overall quality. Order is reversed if argument is `true` ( reverse = true )
        """
        ...
    
    def swap(self, in_0: FeatureMap ) -> None:
        """
        Cython signature: void swap(FeatureMap &)
        """
        ...
    
    def swapFeaturesOnly(self, swapfrom: FeatureMap ) -> None:
        """
        Cython signature: void swapFeaturesOnly(FeatureMap swapfrom)
        Swaps the feature content (plus its range information) of this map
        """
        ...
    
    @overload
    def clear(self, ) -> None:
        """
        Cython signature: void clear()
        Clears all data and meta data
        """
        ...
    
    @overload
    def clear(self, clear_meta_data: bool ) -> None:
        """
        Cython signature: void clear(bool clear_meta_data)
        Clears all data and meta data. If 'true' is passed as an argument, all meta data is cleared in addition to the data
        """
        ...
    
    def __add__(self: FeatureMap, other: FeatureMap) -> FeatureMap:
        ...
    
    def __iadd__(self: FeatureMap, other: FeatureMap) -> FeatureMap:
        ...
    
    def updateRanges(self) -> None:
        """
        Cython signature: void updateRanges()
        """
        ...
    
    def getProteinIdentifications(self) -> List[ProteinIdentification]:
        """
        Cython signature: libcpp_vector[ProteinIdentification] getProteinIdentifications()
        """
        ...
    
    def setProteinIdentifications(self, in_0: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void setProteinIdentifications(libcpp_vector[ProteinIdentification])
        Sets the protein identifications
        """
        ...
    
    def getUnassignedPeptideIdentifications(self) -> List[PeptideIdentification]:
        """
        Cython signature: libcpp_vector[PeptideIdentification] getUnassignedPeptideIdentifications()
        """
        ...
    
    def setUnassignedPeptideIdentifications(self, in_0: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void setUnassignedPeptideIdentifications(libcpp_vector[PeptideIdentification])
        Sets the unassigned peptide identifications
        """
        ...
    
    def getDataProcessing(self) -> List[DataProcessing]:
        """
        Cython signature: libcpp_vector[DataProcessing] getDataProcessing()
        """
        ...
    
    def setDataProcessing(self, in_0: List[DataProcessing] ) -> None:
        """
        Cython signature: void setDataProcessing(libcpp_vector[DataProcessing])
        Sets the description of the applied data processing
        """
        ...
    
    @overload
    def setPrimaryMSRunPath(self, s: List[bytes] ) -> None:
        """
        Cython signature: void setPrimaryMSRunPath(StringList & s)
        Sets the file path to the primary MS run (usually the mzML file obtained after data conversion from raw files)
        """
        ...
    
    @overload
    def setPrimaryMSRunPath(self, s: List[bytes] , e: MSExperiment ) -> None:
        """
        Cython signature: void setPrimaryMSRunPath(StringList & s, MSExperiment & e)
        Sets the file path to the primary MS run using the mzML annotated in the MSExperiment argument `e`
        """
        ...
    
    def getPrimaryMSRunPath(self, toFill: List[bytes] ) -> None:
        """
        Cython signature: void getPrimaryMSRunPath(StringList & toFill)
        Returns the file path to the first MS run
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
    
    def __richcmp__(self, other: FeatureMap, op: int) -> Any:
        ...
    
    def __iter__(self) -> Feature:
       ... 


class FeatureXMLFile:
    """
    Cython implementation of _FeatureXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureXMLFile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureXMLFile()
        This class provides Input/Output functionality for feature maps
        """
        ...
    
    def load(self, in_0: Union[bytes, str, String] , in_1: FeatureMap ) -> None:
        """
        Cython signature: void load(String, FeatureMap &)
        Loads the file with name `filename` into `map` and calls updateRanges()
        """
        ...
    
    def store(self, in_0: Union[bytes, str, String] , in_1: FeatureMap ) -> None:
        """
        Cython signature: void store(String, FeatureMap &)
        Stores the map `feature_map` in file with name `filename`
        """
        ...
    
    def getOptions(self) -> FeatureFileOptions:
        """
        Cython signature: FeatureFileOptions getOptions()
        Access to the options for loading/storing
        """
        ...
    
    def setOptions(self, in_0: FeatureFileOptions ) -> None:
        """
        Cython signature: void setOptions(FeatureFileOptions)
        Setter for options for loading/storing
        """
        ...
    
    def loadSize(self, path: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t loadSize(String path)
        """
        ... 


class File:
    """
    Cython implementation of _File

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1File.html>`_
    """
    
    absolutePath: __static_File_absolutePath
    
    basename: __static_File_basename
    
    empty: __static_File_empty
    
    exists: __static_File_exists
    
    fileList: __static_File_fileList
    
    find: __static_File_find
    
    findDatabase: __static_File_findDatabase
    
    findDoc: __static_File_findDoc
    
    findExecutable: __static_File_findExecutable
    
    getExecutablePath: __static_File_getExecutablePath
    
    getOpenMSDataPath: __static_File_getOpenMSDataPath
    
    getOpenMSHomePath: __static_File_getOpenMSHomePath
    
    getSystemParameters: __static_File_getSystemParameters
    
    getTempDirectory: __static_File_getTempDirectory
    
    getTemporaryFile: __static_File_getTemporaryFile
    
    getUniqueName: __static_File_getUniqueName
    
    getUserDirectory: __static_File_getUserDirectory
    
    isDirectory: __static_File_isDirectory
    
    path: __static_File_path
    
    readable: __static_File_readable
    
    remove: __static_File_remove
    
    removeDirRecursively: __static_File_removeDirRecursively
    
    rename: __static_File_rename
    
    writable: __static_File_writable 


class IDConflictResolverAlgorithm:
    """
    Cython implementation of _IDConflictResolverAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IDConflictResolverAlgorithm.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IDConflictResolverAlgorithm()
        Resolves ambiguous annotations of features with peptide identifications
        """
        ...
    
    @overload
    def __init__(self, in_0: IDConflictResolverAlgorithm ) -> None:
        """
        Cython signature: void IDConflictResolverAlgorithm(IDConflictResolverAlgorithm &)
        """
        ...
    
    @overload
    def resolve(self, features: FeatureMap ) -> None:
        """
        Cython signature: void resolve(FeatureMap & features)
        Resolves ambiguous annotations of features with peptide identifications\n
        
        The the filtered identifications are added to the vector of unassigned peptides
        and also reduced to a single best hit
        
        
        :param keep_matching: Keeps all IDs that match the modified sequence of the best hit in the feature (e.g. keeps all IDs in a ConsensusMap if id'd same across multiple runs)
        """
        ...
    
    @overload
    def resolve(self, features: ConsensusMap ) -> None:
        """
        Cython signature: void resolve(ConsensusMap & features)
        Resolves ambiguous annotations of consensus features with peptide identifications\n
        
        The the filtered identifications are added to the vector of unassigned peptides
        and also reduced to a single best hit
        
        
        :param keep_matching: Keeps all IDs that match the modified sequence of the best hit in the feature (e.g. keeps all IDs in a ConsensusMap if id'd same across multiple runs)
        """
        ...
    
    @overload
    def resolveBetweenFeatures(self, features: FeatureMap ) -> None:
        """
        Cython signature: void resolveBetweenFeatures(FeatureMap & features)
        In a single (feature/consensus) map, features with the same (possibly modified) sequence and charge state may appear\n
        
        This filter removes the peptide sequence annotations from features, if a higher-intensity feature with the same (charge, sequence)
        combination exists in the map. The total number of features remains unchanged. In the final output, each (charge, sequence) combination
        appears only once, i.e. no multiplicities
        """
        ...
    
    @overload
    def resolveBetweenFeatures(self, features: ConsensusMap ) -> None:
        """
        Cython signature: void resolveBetweenFeatures(ConsensusMap & features)
        In a single (feature/consensus) map, features with the same (possibly modified) sequence and charge state may appear\n
        
        This filter removes the peptide sequence annotations from features, if a higher-intensity feature with the same (charge, sequence)
        combination exists in the map. The total number of features remains unchanged. In the final output, each (charge, sequence) combination
        appears only once, i.e. no multiplicities
        """
        ... 


class IDMapper:
    """
    Cython implementation of _IDMapper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IDMapper.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IDMapper()
        Annotates an MSExperiment, FeatureMap or ConsensusMap with peptide identifications
        """
        ...
    
    @overload
    def __init__(self, in_0: IDMapper ) -> None:
        """
        Cython signature: void IDMapper(IDMapper &)
        """
        ...
    
    @overload
    def annotate(self, map_: MSExperiment , ids: List[PeptideIdentification] , protein_ids: List[ProteinIdentification] , clear_ids: bool , mapMS1: bool ) -> None:
        """
        Cython signature: void annotate(MSExperiment & map_, libcpp_vector[PeptideIdentification] & ids, libcpp_vector[ProteinIdentification] & protein_ids, bool clear_ids, bool mapMS1)
        Mapping method for peak maps\n
        
        The identifications stored in a PeptideIdentification instance can be added to the
        corresponding spectrum
        Note that a PeptideIdentication is added to ALL spectra which are within the allowed RT and MZ boundaries
        
        
        :param map: MSExperiment to receive the identifications
        :param peptide_ids: PeptideIdentification for the MSExperiment
        :param protein_ids: ProteinIdentification for the MSExperiment
        :param clear_ids: Reset peptide and protein identifications of each scan before annotating
        :param map_ms1: Attach Ids to MS1 spectra using RT mapping only (without precursor, without m/z)
        :raises:
          Exception: MissingInformation is thrown if entries of 'peptide_ids' do not contain 'MZ' and 'RT' information
        """
        ...
    
    @overload
    def annotate(self, map_: MSExperiment , fmap: FeatureMap , clear_ids: bool , mapMS1: bool ) -> None:
        """
        Cython signature: void annotate(MSExperiment & map_, FeatureMap & fmap, bool clear_ids, bool mapMS1)
        Mapping method for peak maps\n
        
        Add peptide identifications stored in a feature map to their
        corresponding spectrum
        This function converts the feature map to a vector of peptide identifications (all peptide IDs from each feature are taken)
        and calls the respective annotate() function
        RT and m/z are taken from the peptides, or (if missing) from the feature itself
        
        
        :param map: MSExperiment to receive the identifications
        :param fmap: FeatureMap with PeptideIdentifications for the MSExperiment
        :param clear_ids: Reset peptide and protein identifications of each scan before annotating
        :param map_ms1: Attach Ids to MS1 spectra using RT mapping only (without precursor, without m/z)
        """
        ...
    
    @overload
    def annotate(self, map_: FeatureMap , ids: List[PeptideIdentification] , protein_ids: List[ProteinIdentification] , use_centroid_rt: bool , use_centroid_mz: bool , spectra: MSExperiment ) -> None:
        """
        Cython signature: void annotate(FeatureMap & map_, libcpp_vector[PeptideIdentification] & ids, libcpp_vector[ProteinIdentification] & protein_ids, bool use_centroid_rt, bool use_centroid_mz, MSExperiment & spectra)
        Mapping method for peak maps\n
        
        If all features have at least one convex hull, peptide positions are matched against the bounding boxes of the convex hulls by default. If not, the positions of the feature centroids are used. The respective coordinates of the centroids are also used for matching (in place of the corresponding ranges from the bounding boxes) if 'use_centroid_rt' or 'use_centroid_mz' are true\n
        
        In any case, tolerance in RT and m/z dimension is applied according to the global parameters 'rt_tolerance' and 'mz_tolerance'. Tolerance is understood as "plus or minus x", so the matching range is actually increased by twice the tolerance value\n
        
        If several features (incl. tolerance) overlap the position of a peptide identification, the identification is annotated to all of them
        
        
        :param map: MSExperiment to receive the identifications
        :param ids: PeptideIdentification for the MSExperiment
        :param protein_ids: ProteinIdentification for the MSExperiment
        :param use_centroid_rt: Whether to use the RT value of feature centroids even if convex hulls are present
        :param use_centroid_mz: Whether to use the m/z value of feature centroids even if convex hulls are present
        :param spectra: Whether precursors not contained in the identifications are annotated with an empty PeptideIdentification object containing the scan index
        :raises:
          Exception: MissingInformation is thrown if entries of 'ids' do not contain 'MZ' and 'RT' information
        """
        ...
    
    @overload
    def annotate(self, map_: ConsensusMap , ids: List[PeptideIdentification] , protein_ids: List[ProteinIdentification] , measure_from_subelements: bool , annotate_ids_with_subelements: bool , spectra: MSExperiment ) -> None:
        """
        Cython signature: void annotate(ConsensusMap & map_, libcpp_vector[PeptideIdentification] & ids, libcpp_vector[ProteinIdentification] & protein_ids, bool measure_from_subelements, bool annotate_ids_with_subelements, MSExperiment & spectra)
        Mapping method for peak maps\n
        
        If all features have at least one convex hull, peptide positions are matched against the bounding boxes of the convex hulls by default. If not, the positions of the feature centroids are used. The respective coordinates of the centroids are also used for matching (in place of the corresponding ranges from the bounding boxes) if 'use_centroid_rt' or 'use_centroid_mz' are true\n
        
        In any case, tolerance in RT and m/z dimension is applied according to the global parameters 'rt_tolerance' and 'mz_tolerance'. Tolerance is understood as "plus or minus x", so the matching range is actually increased by twice the tolerance value\n
        
        If several features (incl. tolerance) overlap the position of a peptide identification, the identification is annotated to all of them
        
        
        :param map: MSExperiment to receive the identifications
        :param ids: PeptideIdentification for the MSExperiment
        :param protein_ids: ProteinIdentification for the MSExperiment
        :param measure_from_subelements: Boolean operator set to true if distance estimate from FeatureHandles instead of Centroid
        :param annotate_ids_with_subelements: Boolean operator set to true if store map index of FeatureHandle in peptide identification
        :param spectra: Whether precursors not contained in the identifications are annotated with an empty PeptideIdentification object containing the scan index
        :raises:
          Exception: MissingInformation is thrown if entries of 'ids' do not contain 'MZ' and 'RT' information
        """
        ...
    
    def mapPrecursorsToIdentifications(self, spectra: MSExperiment , ids: List[PeptideIdentification] , mz_tol: float , rt_tol: float ) -> IDMapper_SpectraIdentificationState:
        """
        Cython signature: IDMapper_SpectraIdentificationState mapPrecursorsToIdentifications(MSExperiment spectra, libcpp_vector[PeptideIdentification] & ids, double mz_tol, double rt_tol)
        Mapping of peptide identifications to spectra\n
        This helper function partitions all spectra into those that had:
        - no precursor (e.g. MS1 spectra),
        - at least one identified precursor,
        - or only unidentified precursor
        
        
        :param spectra: The mass spectra
        :param ids: The peptide identifications
        :param mz_tol: Tolerance used to map to precursor m/z
        :param rt_tol: Tolerance used to map to spectrum retention time
        :return: A struct of vectors holding spectra indices of the partitioning
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


class IDMapper_SpectraIdentificationState:
    """
    Cython implementation of _IDMapper_SpectraIdentificationState

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IDMapper_SpectraIdentificationState.html>`_
    """
    
    no_precursors: List[int]
    
    identified: List[int]
    
    unidentified: List[int]
    
    def __init__(self) -> None:
        """
        Cython signature: void IDMapper_SpectraIdentificationState()
        """
        ... 


class IDRipper:
    """
    Cython implementation of _IDRipper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1IDRipper.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void IDRipper()
        Ripping protein/peptide identification according their file origin
        """
        ...
    
    def rip(self, rfis: List[RipFileIdentifier] , rfcs: List[RipFileContent] , proteins: List[ProteinIdentification] , peptides: List[PeptideIdentification] , full_split: bool , split_ident_runs: bool ) -> None:
        """
        Cython signature: void rip(libcpp_vector[RipFileIdentifier] & rfis, libcpp_vector[RipFileContent] & rfcs, libcpp_vector[ProteinIdentification] & proteins, libcpp_vector[PeptideIdentification] & peptides, bool full_split, bool split_ident_runs)
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


class ILPDCWrapper:
    """
    Cython implementation of _ILPDCWrapper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ILPDCWrapper.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ILPDCWrapper()
        """
        ...
    
    @overload
    def __init__(self, in_0: ILPDCWrapper ) -> None:
        """
        Cython signature: void ILPDCWrapper(ILPDCWrapper &)
        """
        ...
    
    def compute(self, fm: FeatureMap , pairs: List[ChargePair] , verbose_level: int ) -> float:
        """
        Cython signature: double compute(FeatureMap fm, libcpp_vector[ChargePair] & pairs, size_t verbose_level)
        Compute optimal solution and return value of objective function. If the input feature map is empty, a warning is issued and -1 is returned
        """
        ... 


class IMSAlphabet:
    """
    Cython implementation of _IMSAlphabet

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ims::IMSAlphabet_1_1IMSAlphabet.html>`_

    Holds an indexed list of bio-chemical elements.\n
    
    Presents an indexed list of bio-chemical elements of type (or derived from
    type) 'Element'. Due to indexed structure 'Alphabet' can be used similar
    to std::vector, for example to add a new element to 'Alphabet' function
    push_back(element_type) can be used. Elements or their properties (such
    as element's mass) can be accessed by index in a constant time. On the other
    hand accessing elements by their names takes linear time. Due to this and
    also the fact that 'Alphabet' is 'heavy-weighted' (consisting of
    'Element' -s or their derivatives where the depth of derivation as well is
    undefined resulting in possibly 'heavy' access operations) it is recommended
    not use 'Alphabet' directly in operations where fast access to
    'Element' 's properties is required. Instead consider to use
    'light-weighted' equivalents, such as 'Weights'
    
    
    :param map: MSExperiment to receive the identifications
    :param fmap: FeatureMap with PeptideIdentifications for the MSExperiment
    :param clear_ids: Reset peptide and protein identifications of each scan before annotating
    :param map_ms1: Attach Ids to MS1 spectra using RT mapping only (without precursor, without m/z)
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IMSAlphabet()
        """
        ...
    
    @overload
    def __init__(self, in_0: IMSAlphabet ) -> None:
        """
        Cython signature: void IMSAlphabet(IMSAlphabet &)
        """
        ...
    
    @overload
    def __init__(self, elements: List[IMSElement] ) -> None:
        """
        Cython signature: void IMSAlphabet(libcpp_vector[IMSElement] & elements)
        """
        ...
    
    @overload
    def getElement(self, name: bytes ) -> IMSElement:
        """
        Cython signature: IMSElement getElement(libcpp_string & name)
        Gets the element with 'index' and returns element with the given index in alphabet
        """
        ...
    
    @overload
    def getElement(self, index: int ) -> IMSElement:
        """
        Cython signature: IMSElement getElement(int index)
        Gets the element with 'index'
        """
        ...
    
    def getName(self, index: int ) -> bytes:
        """
        Cython signature: libcpp_string getName(int index)
        Gets the symbol of the element with an 'index' in alphabet
        """
        ...
    
    @overload
    def getMass(self, name: bytes ) -> float:
        """
        Cython signature: double getMass(libcpp_string & name)
        Gets mono isotopic mass of the element with the symbol 'name'
        """
        ...
    
    @overload
    def getMass(self, index: int ) -> float:
        """
        Cython signature: double getMass(int index)
        Gets mass of the element with an 'index' in alphabet
        """
        ...
    
    def getMasses(self, isotope_index: int ) -> List[float]:
        """
        Cython signature: libcpp_vector[double] getMasses(int isotope_index)
        Gets masses of elements isotopes given by 'isotope_index'
        """
        ...
    
    def getAverageMasses(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] getAverageMasses()
        Gets average masses of elements
        """
        ...
    
    def hasName(self, name: bytes ) -> bool:
        """
        Cython signature: bool hasName(libcpp_string & name)
        Returns true if there is an element with symbol 'name' in the alphabet, false - otherwise
        """
        ...
    
    @overload
    def push_back(self, name: bytes , value: float ) -> None:
        """
        Cython signature: void push_back(libcpp_string & name, double value)
        Adds a new element with 'name' and mass 'value'
        """
        ...
    
    @overload
    def push_back(self, element: IMSElement ) -> None:
        """
        Cython signature: void push_back(IMSElement & element)
        Adds a new 'element' to the alphabet
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        Clears the alphabet data
        """
        ...
    
    def sortByNames(self) -> None:
        """
        Cython signature: void sortByNames()
        Sorts the alphabet by names
        """
        ...
    
    def sortByValues(self) -> None:
        """
        Cython signature: void sortByValues()
        Sorts the alphabet by mass values
        """
        ...
    
    def load(self, fname: String ) -> None:
        """
        Cython signature: void load(String & fname)
        Loads the alphabet data from the file 'fname' using the default parser. If there is no file 'fname', throws an 'IOException'
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: int size()
        """
        ...
    
    def setElement(self, name: bytes , mass: float , forced: bool ) -> None:
        """
        Cython signature: void setElement(libcpp_string & name, double mass, bool forced)
        Overwrites an element in the alphabet with the 'name' with a new element constructed from the given 'name' and 'mass'
        """
        ...
    
    def erase(self, name: bytes ) -> bool:
        """
        Cython signature: bool erase(libcpp_string & name)
        Removes the element with 'name' from the alphabet
        """
        ... 


class IMTypes:
    """
    Cython implementation of _IMTypes

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IMTypes.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IMTypes()
        """
        ...
    
    @overload
    def __init__(self, in_0: IMTypes ) -> None:
        """
        Cython signature: void IMTypes(IMTypes &)
        """
        ...
    
    @overload
    def determineIMFormat(self, exp: MSExperiment ) -> int:
        """
        Cython signature: IMFormat determineIMFormat(const MSExperiment & exp)
        """
        ...
    
    @overload
    def determineIMFormat(self, spec: MSSpectrum ) -> int:
        """
        Cython signature: IMFormat determineIMFormat(const MSSpectrum & spec)
        """
        ...
    
    toDriftTimeUnit: __static_IMTypes_toDriftTimeUnit
    
    toIMFormat: __static_IMTypes_toIMFormat
    
    toString: __static_IMTypes_toString
    
    toString: __static_IMTypes_toString 


class IdentificationRuns:
    """
    Cython implementation of _IdentificationRuns

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1IdentificationRuns.html>`_
    """
    
    def __init__(self, prot_ids: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void IdentificationRuns(libcpp_vector[ProteinIdentification] & prot_ids)
        """
        ... 


class IndexedMzMLHandler:
    """
    Cython implementation of _IndexedMzMLHandler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IndexedMzMLHandler.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IndexedMzMLHandler()
        """
        ...
    
    @overload
    def __init__(self, in_0: IndexedMzMLHandler ) -> None:
        """
        Cython signature: void IndexedMzMLHandler(IndexedMzMLHandler &)
        """
        ...
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void IndexedMzMLHandler(String filename)
        """
        ...
    
    def openFile(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void openFile(String filename)
        """
        ...
    
    def getParsingSuccess(self) -> bool:
        """
        Cython signature: bool getParsingSuccess()
        """
        ...
    
    def getNrSpectra(self) -> int:
        """
        Cython signature: size_t getNrSpectra()
        """
        ...
    
    def getNrChromatograms(self) -> int:
        """
        Cython signature: size_t getNrChromatograms()
        """
        ...
    
    def getSpectrumById(self, id_: int ) -> _Interfaces_Spectrum:
        """
        Cython signature: shared_ptr[_Interfaces_Spectrum] getSpectrumById(int id_)
        """
        ...
    
    def getChromatogramById(self, id_: int ) -> _Interfaces_Chromatogram:
        """
        Cython signature: shared_ptr[_Interfaces_Chromatogram] getChromatogramById(int id_)
        """
        ...
    
    def getMSSpectrumById(self, id_: int ) -> MSSpectrum:
        """
        Cython signature: MSSpectrum getMSSpectrumById(int id_)
        """
        ...
    
    def getMSSpectrumByNativeId(self, id_: bytes , spec: MSSpectrum ) -> None:
        """
        Cython signature: void getMSSpectrumByNativeId(libcpp_string id_, MSSpectrum & spec)
        """
        ...
    
    def getMSChromatogramById(self, id_: int ) -> MSChromatogram:
        """
        Cython signature: MSChromatogram getMSChromatogramById(int id_)
        """
        ...
    
    def getMSChromatogramByNativeId(self, id_: bytes , chrom: MSChromatogram ) -> None:
        """
        Cython signature: void getMSChromatogramByNativeId(libcpp_string id_, MSChromatogram & chrom)
        """
        ...
    
    def setSkipXMLChecks(self, skip: bool ) -> None:
        """
        Cython signature: void setSkipXMLChecks(bool skip)
        """
        ... 


class InspectOutfile:
    """
    Cython implementation of _InspectOutfile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1InspectOutfile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void InspectOutfile()
        This class serves to read in an Inspect outfile and write an idXML file
        """
        ...
    
    @overload
    def __init__(self, in_0: InspectOutfile ) -> None:
        """
        Cython signature: void InspectOutfile(InspectOutfile &)
        """
        ...
    
    def load(self, result_filename: Union[bytes, str, String] , peptide_identifications: List[PeptideIdentification] , protein_identification: ProteinIdentification , p_value_threshold: float , database_filename: Union[bytes, str, String] ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] load(const String & result_filename, libcpp_vector[PeptideIdentification] & peptide_identifications, ProteinIdentification & protein_identification, double p_value_threshold, const String & database_filename)
        Load the results of an Inspect search
        
        
        :param result_filename: Input parameter which is the file name of the input file
        :param peptide_identifications: Output parameter which holds the peptide identifications from the given file
        :param protein_identification: Output parameter which holds the protein identifications from the given file
        :param p_value_threshold:
        :param database_filename:
        :raises:
          Exception: FileNotFound is thrown if the given file could not be found
        :raises:
          Exception: ParseError is thrown if the given file could not be parsed
        :raises:
          Exception: FileEmpty is thrown if the given file is empty
        """
        ...
    
    def getWantedRecords(self, result_filename: Union[bytes, str, String] , p_value_threshold: float ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] getWantedRecords(const String & result_filename, double p_value_threshold)
        Loads only results which exceeds a given p-value threshold
        
        
        :param result_filename: The filename of the results file
        :param p_value_threshold: Only identifications exceeding this threshold are read
        :raises:
          Exception: FileNotFound is thrown if the given file could not be found
        :raises:
          Exception: FileEmpty is thrown if the given file is empty
        """
        ...
    
    def compressTrieDB(self, database_filename: Union[bytes, str, String] , index_filename: Union[bytes, str, String] , wanted_records: List[int] , snd_database_filename: Union[bytes, str, String] , snd_index_filename: Union[bytes, str, String] , append: bool ) -> None:
        """
        Cython signature: void compressTrieDB(const String & database_filename, const String & index_filename, libcpp_vector[size_t] & wanted_records, const String & snd_database_filename, const String & snd_index_filename, bool append)
        Generates a trie database from another one, using the wanted records only
        """
        ...
    
    def generateTrieDB(self, source_database_filename: Union[bytes, str, String] , database_filename: Union[bytes, str, String] , index_filename: Union[bytes, str, String] , append: bool , species: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void generateTrieDB(const String & source_database_filename, const String & database_filename, const String & index_filename, bool append, const String species)
        Generates a trie database from a given one (the type of database is determined by getLabels)
        """
        ...
    
    def getACAndACType(self, line: Union[bytes, str, String] , accession: String , accession_type: String ) -> None:
        """
        Cython signature: void getACAndACType(String line, String & accession, String & accession_type)
        Retrieve the accession type and accession number from a protein description line
        """
        ...
    
    def getLabels(self, source_database_filename: Union[bytes, str, String] , ac_label: String , sequence_start_label: String , sequence_end_label: String , comment_label: String , species_label: String ) -> None:
        """
        Cython signature: void getLabels(const String & source_database_filename, String & ac_label, String & sequence_start_label, String & sequence_end_label, String & comment_label, String & species_label)
        Retrieve the labels of a given database (at the moment FASTA and Swissprot)
        """
        ...
    
    def getSequences(self, database_filename: Union[bytes, str, String] , wanted_records: Dict[int, int] , sequences: List[bytes] ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] getSequences(const String & database_filename, libcpp_map[size_t,size_t] & wanted_records, libcpp_vector[String] & sequences)
        Retrieve sequences from a trie database
        """
        ...
    
    def getExperiment(self, exp: MSExperiment , type_: String , in_filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void getExperiment(MSExperiment & exp, String & type_, const String & in_filename)
        Get the experiment from a file
        """
        ...
    
    def getSearchEngineAndVersion(self, cmd_output: Union[bytes, str, String] , protein_identification: ProteinIdentification ) -> bool:
        """
        Cython signature: bool getSearchEngineAndVersion(const String & cmd_output, ProteinIdentification & protein_identification)
        Get the search engine and its version from the output of the InsPecT executable without parameters. Returns true on success, false otherwise
        """
        ...
    
    def readOutHeader(self, filename: Union[bytes, str, String] , header_line: Union[bytes, str, String] , spectrum_file_column: int , scan_column: int , peptide_column: int , protein_column: int , charge_column: int , MQ_score_column: int , p_value_column: int , record_number_column: int , DB_file_pos_column: int , spec_file_pos_column: int , number_of_columns: int ) -> None:
        """
        Cython signature: void readOutHeader(const String & filename, const String & header_line, int & spectrum_file_column, int & scan_column, int & peptide_column, int & protein_column, int & charge_column, int & MQ_score_column, int & p_value_column, int & record_number_column, int & DB_file_pos_column, int & spec_file_pos_column, size_t & number_of_columns)
        Read the header of an inspect output file and retrieve various information
        """
        ...
    
    def __richcmp__(self, other: InspectOutfile, op: int) -> Any:
        ... 


class Internal_MzMLValidator:
    """
    Cython implementation of _Internal_MzMLValidator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1Internal_MzMLValidator.html>`_
    """
    
    def __init__(self, mapping: CVMappings , cv: ControlledVocabulary ) -> None:
        """
        Cython signature: void Internal_MzMLValidator(CVMappings & mapping, ControlledVocabulary & cv)
        """
        ... 


class IonDetector:
    """
    Cython implementation of _IonDetector

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IonDetector.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IonDetector()
        Description of a ion detector (part of a MS Instrument)
        """
        ...
    
    @overload
    def __init__(self, in_0: IonDetector ) -> None:
        """
        Cython signature: void IonDetector(IonDetector &)
        """
        ...
    
    def getType(self) -> int:
        """
        Cython signature: Type_IonDetector getType()
        Returns the detector type
        """
        ...
    
    def setType(self, type_: int ) -> None:
        """
        Cython signature: void setType(Type_IonDetector type_)
        Sets the detector type
        """
        ...
    
    def getAcquisitionMode(self) -> int:
        """
        Cython signature: AcquisitionMode getAcquisitionMode()
        Returns the acquisition mode
        """
        ...
    
    def setAcquisitionMode(self, acquisition_mode: int ) -> None:
        """
        Cython signature: void setAcquisitionMode(AcquisitionMode acquisition_mode)
        Sets the acquisition mode
        """
        ...
    
    def getResolution(self) -> float:
        """
        Cython signature: double getResolution()
        Returns the resolution (in ns)
        """
        ...
    
    def setResolution(self, resolution: float ) -> None:
        """
        Cython signature: void setResolution(double resolution)
        Sets the resolution (in ns)
        """
        ...
    
    def getADCSamplingFrequency(self) -> float:
        """
        Cython signature: double getADCSamplingFrequency()
        Returns the analog-to-digital converter sampling frequency (in Hz)
        """
        ...
    
    def setADCSamplingFrequency(self, ADC_sampling_frequency: float ) -> None:
        """
        Cython signature: void setADCSamplingFrequency(double ADC_sampling_frequency)
        Sets the analog-to-digital converter sampling frequency (in Hz)
        """
        ...
    
    def getOrder(self) -> int:
        """
        Cython signature: int getOrder()
        Returns the order
        """
        ...
    
    def setOrder(self, order: int ) -> None:
        """
        Cython signature: void setOrder(int order)
        Sets the order
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
    
    def __richcmp__(self, other: IonDetector, op: int) -> Any:
        ...
    AcquisitionMode : __AcquisitionMode
    Type_IonDetector : __Type_IonDetector 


class IsobaricQuantifier:
    """
    Cython implementation of _IsobaricQuantifier

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsobaricQuantifier.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, in_0: IsobaricQuantifier ) -> None:
        """
        Cython signature: void IsobaricQuantifier(IsobaricQuantifier &)
        """
        ...
    
    @overload
    def __init__(self, quant_method: ItraqFourPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricQuantifier(ItraqFourPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: ItraqEightPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricQuantifier(ItraqEightPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: TMTSixPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricQuantifier(TMTSixPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: TMTTenPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricQuantifier(TMTTenPlexQuantitationMethod * quant_method)
        """
        ...
    
    def quantify(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap ) -> None:
        """
        Cython signature: void quantify(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out)
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


class IsobaricQuantifierStatistics:
    """
    Cython implementation of _IsobaricQuantifierStatistics

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsobaricQuantifierStatistics.html>`_
    """
    
    channel_count: int
    
    iso_number_ms2_negative: int
    
    iso_number_reporter_negative: int
    
    iso_number_reporter_different: int
    
    iso_solution_different_intensity: float
    
    iso_total_intensity_negative: float
    
    number_ms2_total: int
    
    number_ms2_empty: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IsobaricQuantifierStatistics()
        """
        ...
    
    @overload
    def __init__(self, in_0: IsobaricQuantifierStatistics ) -> None:
        """
        Cython signature: void IsobaricQuantifierStatistics(IsobaricQuantifierStatistics &)
        """
        ...
    
    def reset(self) -> None:
        """
        Cython signature: void reset()
        """
        ... 


class ItraqConstants:
    """
    Cython implementation of _ItraqConstants

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ItraqConstants.html>`_

    Some constants used throughout iTRAQ classes
    
    Constants for iTRAQ experiments and a ChannelInfo structure to store information about a single channel
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ItraqConstants()
        """
        ...
    
    @overload
    def __init__(self, in_0: ItraqConstants ) -> None:
        """
        Cython signature: void ItraqConstants(ItraqConstants &)
        """
        ...
    
    def getIsotopeMatrixAsStringList(self, itraq_type: int , isotope_corrections: List[MatrixDouble] ) -> List[bytes]:
        """
        Cython signature: StringList getIsotopeMatrixAsStringList(int itraq_type, libcpp_vector[MatrixDouble] & isotope_corrections)
        Convert isotope correction matrix to stringlist\n
        
        Each line is converted into a string of the format channel:-2Da/-1Da/+1Da/+2Da ; e.g. '114:0/0.3/4/0'
        Useful for creating parameters or debug output
        
        
        :param itraq_type: Which matrix to stringify. Should be of values from enum ITRAQ_TYPES
        :param isotope_corrections: Vector of the two matrices (4plex, 8plex)
        """
        ...
    
    def updateIsotopeMatrixFromStringList(self, itraq_type: int , channels: List[bytes] , isotope_corrections: List[MatrixDouble] ) -> None:
        """
        Cython signature: void updateIsotopeMatrixFromStringList(int itraq_type, StringList & channels, libcpp_vector[MatrixDouble] & isotope_corrections)
        Convert strings to isotope correction matrix rows\n
        
        Each string of format channel:-2Da/-1Da/+1Da/+2Da ; e.g. '114:0/0.3/4/0'
        is parsed and the corresponding channel(row) in the matrix is updated
        Not all channels need to be present, missing channels will be left untouched
        Useful to update the matrix with user isotope correction values
        
        
        :param itraq_type: Which matrix to stringify. Should be of values from enum ITRAQ_TYPES
        :param channels: New channel isotope values as strings
        :param isotope_corrections: Vector of the two matrices (4plex, 8plex)
        """
        ...
    
    def translateIsotopeMatrix(self, itraq_type: int , isotope_corrections: List[MatrixDouble] ) -> MatrixDouble:
        """
        Cython signature: MatrixDouble translateIsotopeMatrix(int & itraq_type, libcpp_vector[MatrixDouble] & isotope_corrections)
        """
        ... 


class ItraqEightPlexQuantitationMethod:
    """
    Cython implementation of _ItraqEightPlexQuantitationMethod

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ItraqEightPlexQuantitationMethod.html>`_
      -- Inherits from ['IsobaricQuantitationMethod']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ItraqEightPlexQuantitationMethod()
        iTRAQ 8 plex quantitation to be used with the IsobaricQuantitation
        """
        ...
    
    @overload
    def __init__(self, in_0: ItraqEightPlexQuantitationMethod ) -> None:
        """
        Cython signature: void ItraqEightPlexQuantitationMethod(ItraqEightPlexQuantitationMethod &)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        """
        ...
    
    def getChannelInformation(self) -> List[IsobaricChannelInformation]:
        """
        Cython signature: libcpp_vector[IsobaricChannelInformation] getChannelInformation()
        """
        ...
    
    def getNumberOfChannels(self) -> int:
        """
        Cython signature: size_t getNumberOfChannels()
        """
        ...
    
    def getIsotopeCorrectionMatrix(self) -> MatrixDouble:
        """
        Cython signature: MatrixDouble getIsotopeCorrectionMatrix()
        """
        ...
    
    def getReferenceChannel(self) -> int:
        """
        Cython signature: size_t getReferenceChannel()
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
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class LowessSmoothing:
    """
    Cython implementation of _LowessSmoothing

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1LowessSmoothing.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void LowessSmoothing()
        """
        ...
    
    def smoothData(self, x: List[float] , y: List[float] , y_smoothed: List[float] ) -> None:
        """
        Cython signature: void smoothData(libcpp_vector[double] x, libcpp_vector[double] y, libcpp_vector[double] & y_smoothed)
        Smoothing method that receives x and y coordinates (e.g., RT and intensities) and computes smoothed intensities
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


class MSNumpressCoder:
    """
    Cython implementation of _MSNumpressCoder

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSNumpressCoder.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MSNumpressCoder()
        """
        ...
    
    @overload
    def __init__(self, in_0: MSNumpressCoder ) -> None:
        """
        Cython signature: void MSNumpressCoder(MSNumpressCoder &)
        """
        ...
    
    def encodeNP(self, in_: List[float] , result: String , zlib_compression: bool , config: NumpressConfig ) -> None:
        """
        Cython signature: void encodeNP(libcpp_vector[double] in_, String & result, bool zlib_compression, NumpressConfig config)
        Encodes a vector of floating point numbers into a Base64 string using numpress
        
        This code is obtained from the proteowizard implementation
        ./pwiz/pwiz/data/msdata/BinaryDataEncoder.cpp (adapted by Hannes Roest)
        
        This function will first apply the numpress encoding to the data, then
        encode the result in base64 (with optional zlib compression before
        base64 encoding)
        
        :note In case of error, result string is empty
        
        
        :param in: The vector of floating point numbers to be encoded
        :param result: The resulting string
        :param zlib_compression: Whether to apply zlib compression after numpress compression
        :param config: The numpress configuration defining the compression strategy
        """
        ...
    
    def decodeNP(self, in_: Union[bytes, str, String] , out: List[float] , zlib_compression: bool , config: NumpressConfig ) -> None:
        """
        Cython signature: void decodeNP(const String & in_, libcpp_vector[double] & out, bool zlib_compression, NumpressConfig config)
        Decodes a Base64 string to a vector of floating point numbers using numpress
        
        This code is obtained from the proteowizard implementation
        ./pwiz/pwiz/data/msdata/BinaryDataEncoder.cpp (adapted by Hannes Roest)
        
        This function will first decode the input base64 string (with optional
        zlib decompression after decoding) and then apply numpress decoding to
        the data
        
        
        :param in: The base64 encoded string
        :param out: The resulting vector of doubles
        :param zlib_compression: Whether to apply zlib de-compression before numpress de-compression
        :param config: The numpress configuration defining the compression strategy
        :raises:
          Exception: ConversionError if the string cannot be converted
        """
        ...
    
    def encodeNPRaw(self, in_: List[float] , result: String , config: NumpressConfig ) -> None:
        """
        Cython signature: void encodeNPRaw(libcpp_vector[double] in_, String & result, NumpressConfig config)
        Encode the data vector "in" to a raw byte array
        
        :note In case of error, "result" is given back unmodified
        :note The result is not a string but a raw byte array and may contain zero bytes
        
        This performs the raw numpress encoding on a set of data and does no
        Base64 encoding on the result. Therefore the result string is likely
        *unsafe* to handle and is a raw byte array.
        
        Please use the safe versions above unless you need access to the raw
        byte arrays
        
        
        :param in: The vector of floating point numbers to be encoded
        :param result: The resulting string
        :param config: The numpress configuration defining the compression strategy
        """
        ...
    
    def decodeNPRaw(self, in_: Union[bytes, str, String] , out: List[float] , config: NumpressConfig ) -> None:
        """
        Cython signature: void decodeNPRaw(const String & in_, libcpp_vector[double] & out, NumpressConfig config)
        Decode the raw byte array "in" to the result vector "out"
        
        :note The string in should *only* contain the data and _no_ extra
        null terminating byte
        
        This performs the raw numpress decoding on a raw byte array (not Base64
        encoded). Therefore the input string is likely *unsafe* to handle and is
        basically a byte container
        
        Please use the safe versions above unless you need access to the raw
        byte arrays
        
        
        :param in: The base64 encoded string
        :param out: The resulting vector of doubles
        :param config: The numpress configuration defining the compression strategy
        """
        ...
    NumpressCompression : __NumpressCompression 


class MapAlignmentAlgorithmPoseClustering:
    """
    Cython implementation of _MapAlignmentAlgorithmPoseClustering

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MapAlignmentAlgorithmPoseClustering.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void MapAlignmentAlgorithmPoseClustering()
        """
        ...
    
    @overload
    def align(self, in_0: FeatureMap , in_1: TransformationDescription ) -> None:
        """
        Cython signature: void align(FeatureMap, TransformationDescription &)
        """
        ...
    
    @overload
    def align(self, in_0: MSExperiment , in_1: TransformationDescription ) -> None:
        """
        Cython signature: void align(MSExperiment, TransformationDescription &)
        """
        ...
    
    @overload
    def setReference(self, in_0: FeatureMap ) -> None:
        """
        Cython signature: void setReference(FeatureMap)
        Sets the reference for the alignment
        """
        ...
    
    @overload
    def setReference(self, in_0: MSExperiment ) -> None:
        """
        Cython signature: void setReference(MSExperiment)
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


class MascotXMLFile:
    """
    Cython implementation of _MascotXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MascotXMLFile.html>`_
      -- Inherits from ['XMLFile']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MascotXMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MascotXMLFile ) -> None:
        """
        Cython signature: void MascotXMLFile(MascotXMLFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , protein_identification: ProteinIdentification , id_data: List[PeptideIdentification] , rt_mapping: SpectrumMetaDataLookup ) -> None:
        """
        Cython signature: void load(const String & filename, ProteinIdentification & protein_identification, libcpp_vector[PeptideIdentification] & id_data, SpectrumMetaDataLookup & rt_mapping)
        Loads data from a Mascot XML file
        
        
        :param filename: The file to be loaded
        :param protein_identification: Protein identifications belonging to the whole experiment
        :param id_data: The identifications with m/z and RT
        :param lookup: Helper object for looking up spectrum meta data
        :raises:
          Exception: FileNotFound is thrown if the file does not exists
        :raises:
          Exception: ParseError is thrown if the file does not suit to the standard
        """
        ...
    
    def initializeLookup(self, lookup: SpectrumMetaDataLookup , experiment: MSExperiment , scan_regex: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void initializeLookup(SpectrumMetaDataLookup & lookup, MSExperiment & experiment, const String & scan_regex)
        Initializes a helper object for looking up spectrum meta data (RT, m/z)
        
        
        :param lookup: Helper object to initialize
        :param experiment: Experiment containing the spectra
        :param scan_regex: Optional regular expression for extracting information from references to spectra
        """
        ...
    
    def getVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVersion()
        Return the version of the schema
        """
        ... 


class MetaboliteSpectralMatching:
    """
    Cython implementation of _MetaboliteSpectralMatching

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaboliteSpectralMatching.html>`_
      -- Inherits from ['ProgressLogger', 'DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaboliteSpectralMatching()
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaboliteSpectralMatching ) -> None:
        """
        Cython signature: void MetaboliteSpectralMatching(MetaboliteSpectralMatching &)
        """
        ...
    
    def run(self, exp: MSExperiment , speclib: MSExperiment , mz_tab: MzTab , out_spectra: String ) -> None:
        """
        Cython signature: void run(MSExperiment & exp, MSExperiment & speclib, MzTab & mz_tab, String & out_spectra)
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
    
    computeHyperScore: __static_MetaboliteSpectralMatching_computeHyperScore 


class ModifiedPeptideGenerator:
    """
    Cython implementation of _ModifiedPeptideGenerator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ModifiedPeptideGenerator.html>`_

    Generates modified peptides/proteins.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ModifiedPeptideGenerator()
        """
        ...
    
    @overload
    def __init__(self, in_0: ModifiedPeptideGenerator ) -> None:
        """
        Cython signature: void ModifiedPeptideGenerator(ModifiedPeptideGenerator &)
        """
        ...
    
    @staticmethod
    def getModifications(modNames: List[bytes] ) -> ModifiedPeptideGenerator_MapToResidueType:
        """
        Cython signature: ModifiedPeptideGenerator_MapToResidueType getModifications(const StringList & modNames)
        """
        ...
    
    @staticmethod
    def applyFixedModifications(fixed_mods: ModifiedPeptideGenerator_MapToResidueType , peptide: AASequence ) -> None:
        """
        Cython signature: void applyFixedModifications(const ModifiedPeptideGenerator_MapToResidueType & fixed_mods, AASequence & peptide)
        """
        ...
    
    @staticmethod
    def applyVariableModifications(var_mods: ModifiedPeptideGenerator_MapToResidueType , peptide: AASequence , max_variable_mods_per_peptide: int , all_modified_peptides: List[AASequence] , keep_original: bool ) -> None:
        """
        Cython signature: void applyVariableModifications(const ModifiedPeptideGenerator_MapToResidueType & var_mods, const AASequence & peptide, size_t max_variable_mods_per_peptide, libcpp_vector[AASequence] & all_modified_peptides, bool keep_original)
        """
        ... 


class ModifiedPeptideGenerator_MapToResidueType:
    """
    Cython implementation of _ModifiedPeptideGenerator_MapToResidueType

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ModifiedPeptideGenerator_MapToResidueType.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ModifiedPeptideGenerator_MapToResidueType()
        """
        ...
    
    @overload
    def __init__(self, in_0: ModifiedPeptideGenerator_MapToResidueType ) -> None:
        """
        Cython signature: void ModifiedPeptideGenerator_MapToResidueType(ModifiedPeptideGenerator_MapToResidueType &)
        """
        ... 


class MultiplexDeltaMassesGenerator:
    """
    Cython implementation of _MultiplexDeltaMassesGenerator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MultiplexDeltaMassesGenerator.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MultiplexDeltaMassesGenerator()
        """
        ...
    
    @overload
    def __init__(self, in_0: MultiplexDeltaMassesGenerator ) -> None:
        """
        Cython signature: void MultiplexDeltaMassesGenerator(MultiplexDeltaMassesGenerator &)
        """
        ...
    
    @overload
    def __init__(self, labels: Union[bytes, str, String] , missed_cleavages: int , label_mass_shift: Dict[Union[bytes, str, String], float] ) -> None:
        """
        Cython signature: void MultiplexDeltaMassesGenerator(String labels, int missed_cleavages, libcpp_map[String,double] label_mass_shift)
        """
        ...
    
    def generateKnockoutDeltaMasses(self) -> None:
        """
        Cython signature: void generateKnockoutDeltaMasses()
        """
        ...
    
    def getDeltaMassesList(self) -> List[MultiplexDeltaMasses]:
        """
        Cython signature: libcpp_vector[MultiplexDeltaMasses] getDeltaMassesList()
        """
        ...
    
    def getLabelShort(self, label: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String getLabelShort(String label)
        """
        ...
    
    def getLabelLong(self, label: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String getLabelLong(String label)
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


class MultiplexDeltaMassesGenerator_Label:
    """
    Cython implementation of _MultiplexDeltaMassesGenerator_Label

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MultiplexDeltaMassesGenerator_Label.html>`_
    """
    
    short_name: Union[bytes, str, String]
    
    long_name: Union[bytes, str, String]
    
    description: Union[bytes, str, String]
    
    delta_mass: float
    
    def __init__(self, sn: Union[bytes, str, String] , ln: Union[bytes, str, String] , d: Union[bytes, str, String] , dm: float ) -> None:
        """
        Cython signature: void MultiplexDeltaMassesGenerator_Label(String sn, String ln, String d, double dm)
        """
        ... 


class MzMLSwathFileConsumer:
    """
    Cython implementation of _MzMLSwathFileConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzMLSwathFileConsumer.html>`_
      -- Inherits from ['FullSwathFileConsumer']
    """
    
    @overload
    def __init__(self, in_0: MzMLSwathFileConsumer ) -> None:
        """
        Cython signature: void MzMLSwathFileConsumer(MzMLSwathFileConsumer)
        """
        ...
    
    @overload
    def __init__(self, cachedir: Union[bytes, str, String] , basename: Union[bytes, str, String] , nr_ms1_spectra: int , nr_ms2_spectra: List[int] ) -> None:
        """
        Cython signature: void MzMLSwathFileConsumer(String cachedir, String basename, size_t nr_ms1_spectra, libcpp_vector[int] nr_ms2_spectra)
        """
        ...
    
    @overload
    def __init__(self, known_window_boundaries: List[SwathMap] , cachedir: Union[bytes, str, String] , basename: Union[bytes, str, String] , nr_ms1_spectra: int , nr_ms2_spectra: List[int] ) -> None:
        """
        Cython signature: void MzMLSwathFileConsumer(libcpp_vector[SwathMap] known_window_boundaries, String cachedir, String basename, size_t nr_ms1_spectra, libcpp_vector[int] nr_ms2_spectra)
        """
        ...
    
    def setExpectedSize(self, s: int , c: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t s, size_t c)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings exp)
        """
        ...
    
    def retrieveSwathMaps(self, maps: List[SwathMap] ) -> None:
        """
        Cython signature: void retrieveSwathMaps(libcpp_vector[SwathMap] & maps)
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
        """
        ... 


class MzTabFile:
    """
    Cython implementation of _MzTabFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzTabFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzTabFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MzTabFile ) -> None:
        """
        Cython signature: void MzTabFile(MzTabFile &)
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , mz_tab: MzTab ) -> None:
        """
        Cython signature: void store(String filename, MzTab & mz_tab)
        Stores MzTab file
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , mz_tab: MzTab ) -> None:
        """
        Cython signature: void load(String filename, MzTab & mz_tab)
        Loads MzTab file
        """
        ... 


class MzTabMFile:
    """
    Cython implementation of _MzTabMFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzTabMFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzTabMFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MzTabMFile ) -> None:
        """
        Cython signature: void MzTabMFile(MzTabMFile &)
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , mztab_m: MzTabM ) -> None:
        """
        Cython signature: void store(String filename, MzTabM & mztab_m)
        Store MzTabM file
        """
        ... 


class NonNegativeLeastSquaresSolver:
    """
    Cython implementation of _NonNegativeLeastSquaresSolver

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1NonNegativeLeastSquaresSolver.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void NonNegativeLeastSquaresSolver()
        """
        ...
    
    @overload
    def __init__(self, in_0: NonNegativeLeastSquaresSolver ) -> None:
        """
        Cython signature: void NonNegativeLeastSquaresSolver(NonNegativeLeastSquaresSolver &)
        """
        ...
    
    def solve(self, A: MatrixDouble , b: MatrixDouble , x: MatrixDouble ) -> int:
        """
        Cython signature: int solve(MatrixDouble & A, MatrixDouble & b, MatrixDouble & x)
        """
        ...
    RETURN_STATUS : __RETURN_STATUS 


class NoopMSDataWritingConsumer:
    """
    Cython implementation of _NoopMSDataWritingConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1NoopMSDataWritingConsumer.html>`_

    Consumer class that perform no operation
    
    This is sometimes necessary to fulfill the requirement of passing an
    valid MSDataWritingConsumer object or pointer but no operation is
    required
    """
    
    def __init__(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void NoopMSDataWritingConsumer(String filename)
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
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
    
    def addDataProcessing(self, d: DataProcessing ) -> None:
        """
        Cython signature: void addDataProcessing(DataProcessing d)
        """
        ...
    
    def getNrSpectraWritten(self) -> int:
        """
        Cython signature: size_t getNrSpectraWritten()
        """
        ...
    
    def getNrChromatogramsWritten(self) -> int:
        """
        Cython signature: size_t getNrChromatogramsWritten()
        """
        ... 


class NumpressConfig:
    """
    Cython implementation of _NumpressConfig

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1NumpressConfig.html>`_
    """
    
    numpressFixedPoint: float
    
    numpressErrorTolerance: float
    
    np_compression: int
    
    estimate_fixed_point: bool
    
    linear_fp_mass_acc: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void NumpressConfig()
        """
        ...
    
    @overload
    def __init__(self, in_0: NumpressConfig ) -> None:
        """
        Cython signature: void NumpressConfig(NumpressConfig &)
        """
        ...
    
    def setCompression(self, compression: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCompression(const String & compression)
        """
        ... 


class OpenSwathHelper:
    """
    Cython implementation of _OpenSwathHelper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OpenSwathHelper.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OpenSwathHelper()
        """
        ...
    
    @overload
    def __init__(self, in_0: OpenSwathHelper ) -> None:
        """
        Cython signature: void OpenSwathHelper(OpenSwathHelper &)
        """
        ...
    
    def checkSwathMapAndSelectTransitions(self, exp: MSExperiment , targeted_exp: TargetedExperiment , transition_exp_used: TargetedExperiment , min_upper_edge_dist: float ) -> bool:
        """
        Cython signature: bool checkSwathMapAndSelectTransitions(MSExperiment & exp, TargetedExperiment & targeted_exp, TargetedExperiment & transition_exp_used, double min_upper_edge_dist)
        """
        ...
    
    def estimateRTRange(self, exp: LightTargetedExperiment ) -> List[float, float]:
        """
        Cython signature: libcpp_pair[double,double] estimateRTRange(LightTargetedExperiment exp)
        Computes the min and max retention time value
        
        Estimate the retention time span of a targeted experiment by returning the min/max values in retention time as a pair
        
        
        :return: A std `pair` that contains (min,max)
        """
        ...
    
    def computePrecursorId(self, transition_group_id: Union[bytes, str, String] , isotope: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String computePrecursorId(const String & transition_group_id, int isotope)
        Computes unique precursor identifier
        
        Uses transition_group_id and isotope number to compute a unique precursor
        id of the form "groupID_Precursor_ix" where x is the isotope number, e.g.
        the monoisotopic precursor would become "groupID_Precursor_i0"
        
        
        :param transition_group_id: Unique id of the transition group (peptide/compound)
        :param isotope: Precursor isotope number
        :return: Unique precursor identifier
        """
        ... 


class PlainMSDataWritingConsumer:
    """
    Cython implementation of _PlainMSDataWritingConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PlainMSDataWritingConsumer.html>`_
    """
    
    def __init__(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void PlainMSDataWritingConsumer(String filename)
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings & exp)
        Set experimental settings for the whole file
        
        
        :param exp: Experimental settings to be used for this file (from this and the first spectrum/chromatogram, the class will deduce most of the header of the mzML file)
        """
        ...
    
    def setExpectedSize(self, expectedSpectra: int , expectedChromatograms: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t expectedSpectra, size_t expectedChromatograms)
        Set expected size of spectra and chromatograms to be written
        
        These numbers will be written in the spectrumList and chromatogramList
        tag in the mzML file. Therefore, these will contain wrong numbers if
        the expected size is not set correctly
        
        
        :param expectedSpectra: Number of spectra expected
        :param expectedChromatograms: Number of chromatograms expected
        """
        ...
    
    def addDataProcessing(self, d: DataProcessing ) -> None:
        """
        Cython signature: void addDataProcessing(DataProcessing d)
        Optionally add a data processing method to each chromatogram and spectrum
        
        The provided DataProcessing object will be added to each chromatogram
        and spectrum written to to the mzML file
        
        
        :param d: The DataProcessing object to be added
        """
        ...
    
    def getNrSpectraWritten(self) -> int:
        """
        Cython signature: size_t getNrSpectraWritten()
        Returns the number of spectra written
        """
        ...
    
    def getNrChromatogramsWritten(self) -> int:
        """
        Cython signature: size_t getNrChromatogramsWritten()
        Returns the number of chromatograms written
        """
        ...
    
    def setOptions(self, opt: PeakFileOptions ) -> None:
        """
        Cython signature: void setOptions(PeakFileOptions opt)
        """
        ...
    
    def getOptions(self) -> PeakFileOptions:
        """
        Cython signature: PeakFileOptions getOptions()
        """
        ... 


class RANSAC:
    """
    Cython implementation of _RANSAC[_RansacModelLinear]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1RANSAC[_RansacModelLinear].html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RANSAC()
        """
        ...
    
    @overload
    def __init__(self, seed: int ) -> None:
        """
        Cython signature: void RANSAC(uint64_t seed)
        """
        ...
    
    def ransac(self, pairs: List[List[float, float]] , n: int , k: int , t: float , d: int , relative_d: bool ) -> List[List[float, float]]:
        """
        Cython signature: libcpp_vector[libcpp_pair[double,double]] ransac(libcpp_vector[libcpp_pair[double,double]] pairs, size_t n, size_t k, double t, size_t d, bool relative_d)
        """
        ... 


class RANSACParam:
    """
    Cython implementation of _RANSACParam

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1RANSACParam.html>`_
    """
    
    n: int
    
    k: int
    
    t: float
    
    d: int
    
    relative_d: bool
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RANSACParam()
        A simple struct to carry all the parameters required for a RANSAC run
        """
        ...
    
    @overload
    def __init__(self, p_n: int , p_k: int , p_t: float , p_d: int , p_relative_d: bool ) -> None:
        """
        Cython signature: void RANSACParam(size_t p_n, size_t p_k, double p_t, size_t p_d, bool p_relative_d)
        """
        ...
    
    def toString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        """
        ...
    
    def __str__(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        """
        ... 


class RANSACQuadratic:
    """
    Cython implementation of _RANSAC[_RansacModelQuadratic]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1RANSAC[_RansacModelQuadratic].html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RANSACQuadratic()
        """
        ...
    
    @overload
    def __init__(self, seed: int ) -> None:
        """
        Cython signature: void RANSACQuadratic(uint64_t seed)
        """
        ...
    
    def ransac(self, pairs: List[List[float, float]] , n: int , k: int , t: float , d: int , relative_d: bool ) -> List[List[float, float]]:
        """
        Cython signature: libcpp_vector[libcpp_pair[double,double]] ransac(libcpp_vector[libcpp_pair[double,double]] pairs, size_t n, size_t k, double t, size_t d, bool relative_d)
        """
        ... 


class RealMassDecomposer:
    """
    Cython implementation of _RealMassDecomposer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ims_1_1RealMassDecomposer.html>`_
    """
    
    @overload
    def __init__(self, in_0: RealMassDecomposer ) -> None:
        """
        Cython signature: void RealMassDecomposer(RealMassDecomposer)
        """
        ...
    
    @overload
    def __init__(self, weights: IMSWeights ) -> None:
        """
        Cython signature: void RealMassDecomposer(IMSWeights & weights)
        """
        ...
    
    def getNumberOfDecompositions(self, mass: float , error: float ) -> int:
        """
        Cython signature: uint64_t getNumberOfDecompositions(double mass, double error)
        Gets a number of all decompositions for amass with an error
        allowed. It's similar to thegetDecompositions(double,double) function
        but less space consuming, since doesn't use container to store decompositions
        
        
        :param mass: Mass to be decomposed
        :param error: Error allowed between given and result decomposition
        :return: Number of all decompositions for a given mass and error
        """
        ... 


class RegularSwathFileConsumer:
    """
    Cython implementation of _RegularSwathFileConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1RegularSwathFileConsumer.html>`_
      -- Inherits from ['FullSwathFileConsumer']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RegularSwathFileConsumer()
        """
        ...
    
    @overload
    def __init__(self, in_0: RegularSwathFileConsumer ) -> None:
        """
        Cython signature: void RegularSwathFileConsumer(RegularSwathFileConsumer &)
        """
        ...
    
    def setExpectedSize(self, s: int , c: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t s, size_t c)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings exp)
        """
        ...
    
    def retrieveSwathMaps(self, maps: List[SwathMap] ) -> None:
        """
        Cython signature: void retrieveSwathMaps(libcpp_vector[SwathMap] & maps)
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
        """
        ... 


class Ribonucleotide:
    """
    Cython implementation of _Ribonucleotide

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Ribonucleotide_1_1Ribonucleotide.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Ribonucleotide()
        """
        ...
    
    @overload
    def __init__(self, in_0: Ribonucleotide ) -> None:
        """
        Cython signature: void Ribonucleotide(Ribonucleotide &)
        """
        ...
    
    @overload
    def __init__(self, name: Union[bytes, str, String] , code: Union[bytes, str, String] , new_code: Union[bytes, str, String] , html_code: Union[bytes, str, String] , formula: EmpiricalFormula , origin: bytes , mono_mass: float , avg_mass: float , term_spec: int , baseloss_formula: EmpiricalFormula ) -> None:
        """
        Cython signature: void Ribonucleotide(String name, String code, String new_code, String html_code, EmpiricalFormula formula, char origin, double mono_mass, double avg_mass, TermSpecificityNuc term_spec, EmpiricalFormula baseloss_formula)
        """
        ...
    
    def getCode(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCode()
        Returns the short name
        """
        ...
    
    def setCode(self, code: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCode(String code)
        Sets the short name
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the name of the ribonucleotide
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the ribonucleotide
        """
        ...
    
    def setFormula(self, formula: EmpiricalFormula ) -> None:
        """
        Cython signature: void setFormula(EmpiricalFormula formula)
        Sets empirical formula of the ribonucleotide (must be full, with N and C-terminus)
        """
        ...
    
    def getFormula(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getFormula()
        Returns the empirical formula of the residue
        """
        ...
    
    def setAvgMass(self, avg_mass: float ) -> None:
        """
        Cython signature: void setAvgMass(double avg_mass)
        Sets average mass of the ribonucleotide
        """
        ...
    
    def getAvgMass(self) -> float:
        """
        Cython signature: double getAvgMass()
        Returns average mass of the ribonucleotide
        """
        ...
    
    def setMonoMass(self, mono_mass: float ) -> None:
        """
        Cython signature: void setMonoMass(double mono_mass)
        Sets monoisotopic mass of the ribonucleotide
        """
        ...
    
    def getMonoMass(self) -> float:
        """
        Cython signature: double getMonoMass()
        Returns monoisotopic mass of the ribonucleotide
        """
        ...
    
    def getNewCode(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNewCode()
        Returns the new code
        """
        ...
    
    def setNewCode(self, code: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNewCode(String code)
        Sets the new code
        """
        ...
    
    def getOrigin(self) -> bytes:
        """
        Cython signature: char getOrigin()
        Returns the code of the unmodified base (e.g., "A", "C", ...)
        """
        ...
    
    def setOrigin(self, origin: bytes ) -> None:
        """
        Cython signature: void setOrigin(char origin)
        Sets the code of the unmodified base (e.g., "A", "C", ...)
        """
        ...
    
    def setHTMLCode(self, html_code: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setHTMLCode(String html_code)
        Sets the HTML (RNAMods) code
        """
        ...
    
    def getHTMLCode(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getHTMLCode()
        Returns the HTML (RNAMods) code
        """
        ...
    
    def setTermSpecificity(self, term_spec: int ) -> None:
        """
        Cython signature: void setTermSpecificity(TermSpecificityNuc term_spec)
        Sets the terminal specificity
        """
        ...
    
    def getTermSpecificity(self) -> int:
        """
        Cython signature: TermSpecificityNuc getTermSpecificity()
        Returns the terminal specificity
        """
        ...
    
    def getBaselossFormula(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getBaselossFormula()
        Returns sum formula after loss of the nucleobase
        """
        ...
    
    def setBaselossFormula(self, formula: EmpiricalFormula ) -> None:
        """
        Cython signature: void setBaselossFormula(EmpiricalFormula formula)
        Sets sum formula after loss of the nucleobase
        """
        ...
    
    def isModified(self) -> bool:
        """
        Cython signature: bool isModified()
        True if the ribonucleotide is a modified one
        """
        ...
    
    def __richcmp__(self, other: Ribonucleotide, op: int) -> Any:
        ... 


class RichPeak2D:
    """
    Cython implementation of _RichPeak2D

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1RichPeak2D.html>`_
      -- Inherits from ['Peak2D', 'UniqueIdInterface', 'MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RichPeak2D()
        A 2-dimensional raw data point or peak with meta information
        """
        ...
    
    @overload
    def __init__(self, in_0: RichPeak2D ) -> None:
        """
        Cython signature: void RichPeak2D(RichPeak2D &)
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
    
    def __richcmp__(self, other: RichPeak2D, op: int) -> Any:
        ... 


class RipFileContent:
    """
    Cython implementation of _RipFileContent

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1RipFileContent.html>`_
    """
    
    def __init__(self, prot_idents: List[ProteinIdentification] , pep_idents: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void RipFileContent(libcpp_vector[ProteinIdentification] & prot_idents, libcpp_vector[PeptideIdentification] & pep_idents)
        """
        ...
    
    def getProteinIdentifications(self) -> List[ProteinIdentification]:
        """
        Cython signature: libcpp_vector[ProteinIdentification] getProteinIdentifications()
        """
        ...
    
    def getPeptideIdentifications(self) -> List[PeptideIdentification]:
        """
        Cython signature: libcpp_vector[PeptideIdentification] getPeptideIdentifications()
        """
        ... 


class RipFileIdentifier:
    """
    Cython implementation of _RipFileIdentifier

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1RipFileIdentifier.html>`_
    """
    
    def __init__(self, id_runs: IdentificationRuns , pep_id: PeptideIdentification , file_origin_map: Dict[Union[bytes, str, String], int] , origin_annotation_fmt: int , split_ident_runs: bool ) -> None:
        """
        Cython signature: void RipFileIdentifier(IdentificationRuns & id_runs, PeptideIdentification & pep_id, libcpp_map[String,unsigned int] & file_origin_map, OriginAnnotationFormat origin_annotation_fmt, bool split_ident_runs)
        """
        ...
    
    def getIdentRunIdx(self) -> int:
        """
        Cython signature: unsigned int getIdentRunIdx()
        """
        ...
    
    def getFileOriginIdx(self) -> int:
        """
        Cython signature: unsigned int getFileOriginIdx()
        """
        ...
    
    def getOriginFullname(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOriginFullname()
        """
        ...
    
    def getOutputBasename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOutputBasename()
        """
        ... 


class ScanWindow:
    """
    Cython implementation of _ScanWindow

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ScanWindow.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    begin: float
    
    end: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ScanWindow()
        """
        ...
    
    @overload
    def __init__(self, in_0: ScanWindow ) -> None:
        """
        Cython signature: void ScanWindow(ScanWindow &)
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
    
    def __richcmp__(self, other: ScanWindow, op: int) -> Any:
        ... 


class SpectralMatch:
    """
    Cython implementation of _SpectralMatch

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectralMatch.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectralMatch()
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectralMatch ) -> None:
        """
        Cython signature: void SpectralMatch(SpectralMatch &)
        """
        ...
    
    def getObservedPrecursorMass(self) -> float:
        """
        Cython signature: double getObservedPrecursorMass()
        """
        ...
    
    def setObservedPrecursorMass(self, in_0: float ) -> None:
        """
        Cython signature: void setObservedPrecursorMass(double)
        """
        ...
    
    def getObservedPrecursorRT(self) -> float:
        """
        Cython signature: double getObservedPrecursorRT()
        """
        ...
    
    def setObservedPrecursorRT(self, in_0: float ) -> None:
        """
        Cython signature: void setObservedPrecursorRT(double)
        """
        ...
    
    def getFoundPrecursorMass(self) -> float:
        """
        Cython signature: double getFoundPrecursorMass()
        """
        ...
    
    def setFoundPrecursorMass(self, in_0: float ) -> None:
        """
        Cython signature: void setFoundPrecursorMass(double)
        """
        ...
    
    def getFoundPrecursorCharge(self) -> int:
        """
        Cython signature: int getFoundPrecursorCharge()
        """
        ...
    
    def setFoundPrecursorCharge(self, in_0: int ) -> None:
        """
        Cython signature: void setFoundPrecursorCharge(int)
        """
        ...
    
    def getMatchingScore(self) -> float:
        """
        Cython signature: double getMatchingScore()
        """
        ...
    
    def setMatchingScore(self, in_0: float ) -> None:
        """
        Cython signature: void setMatchingScore(double)
        """
        ...
    
    def getObservedSpectrumIndex(self) -> int:
        """
        Cython signature: size_t getObservedSpectrumIndex()
        """
        ...
    
    def setObservedSpectrumIndex(self, in_0: int ) -> None:
        """
        Cython signature: void setObservedSpectrumIndex(size_t)
        """
        ...
    
    def getMatchingSpectrumIndex(self) -> int:
        """
        Cython signature: size_t getMatchingSpectrumIndex()
        """
        ...
    
    def setMatchingSpectrumIndex(self, in_0: int ) -> None:
        """
        Cython signature: void setMatchingSpectrumIndex(size_t)
        """
        ...
    
    def getPrimaryIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getPrimaryIdentifier()
        """
        ...
    
    def setPrimaryIdentifier(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setPrimaryIdentifier(String)
        """
        ...
    
    def getSecondaryIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSecondaryIdentifier()
        """
        ...
    
    def setSecondaryIdentifier(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSecondaryIdentifier(String)
        """
        ...
    
    def getCommonName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCommonName()
        """
        ...
    
    def setCommonName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCommonName(String)
        """
        ...
    
    def getSumFormula(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSumFormula()
        """
        ...
    
    def setSumFormula(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSumFormula(String)
        """
        ...
    
    def getInchiString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getInchiString()
        """
        ...
    
    def setInchiString(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setInchiString(String)
        """
        ...
    
    def getSMILESString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSMILESString()
        """
        ...
    
    def setSMILESString(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSMILESString(String)
        """
        ...
    
    def getPrecursorAdduct(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getPrecursorAdduct()
        """
        ...
    
    def setPrecursorAdduct(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setPrecursorAdduct(String)
        """
        ... 


class SpectrumAlignmentScore:
    """
    Cython implementation of _SpectrumAlignmentScore

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumAlignmentScore.html>`_
      -- Inherits from ['DefaultParamHandler']

    Similarity score via spectra alignment
    
    This class implements a simple scoring based on the alignment of spectra. This alignment
    is implemented in the SpectrumAlignment class and performs a dynamic programming alignment
    of the peaks, minimizing the distances between the aligned peaks and maximizing the number
    of peak pairs
    
    The scoring is done via the simple formula score = sum / (sqrt(sum1 * sum2)). sum is the
    product of the intensities of the aligned peaks, with the given exponent (default is 2)
    sum1 and sum2 are the sum of the intensities squared for each peak of both spectra respectively
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectrumAlignmentScore()
        Similarity score via spectra alignment
        
        This class implements a simple scoring based on the alignment of spectra. This alignment
        is implemented in the SpectrumAlignment class and performs a dynamic programming alignment
        of the peaks, minimizing the distances between the aligned peaks and maximizing the number
        of peak pairs
        
        The scoring is done via the simple formula score = sum / (sqrt(sum1 * sum2)). sum is the
        product of the intensities of the aligned peaks, with the given exponent (default is 2)
        sum1 and sum2 are the sum of the intensities squared for each peak of both spectra respectively
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAlignmentScore ) -> None:
        """
        Cython signature: void SpectrumAlignmentScore(SpectrumAlignmentScore &)
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


class SqMassConfig:
    """
    Cython implementation of _SqMassConfig

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SqMassConfig.html>`_
    """
    
    write_full_meta: bool
    
    use_lossy_numpress: bool
    
    linear_fp_mass_acc: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SqMassConfig()
        """
        ...
    
    @overload
    def __init__(self, in_0: SqMassConfig ) -> None:
        """
        Cython signature: void SqMassConfig(SqMassConfig &)
        """
        ... 


class SqMassFile:
    """
    Cython implementation of _SqMassFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SqMassFile.html>`_

    An class that uses on-disk SQLite database to read and write spectra and chromatograms
    
    This class provides functions to read and write spectra and chromatograms
    to disk using a SQLite database and store them in sqMass format. This
    allows users to access, select and filter spectra and chromatograms
    on-demand even in a large collection of data
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SqMassFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: SqMassFile ) -> None:
        """
        Cython signature: void SqMassFile(SqMassFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , map_: MSExperiment ) -> None:
        """
        Cython signature: void load(const String & filename, MSExperiment & map_)
        Read / Write a complete mass spectrometric experiment
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , map_: MSExperiment ) -> None:
        """
        Cython signature: void store(const String & filename, MSExperiment & map_)
        Store an MSExperiment in sqMass format
        """
        ...
    
    def setConfig(self, config: SqMassConfig ) -> None:
        """
        Cython signature: void setConfig(SqMassConfig config)
        """
        ... 


class StringView:
    """
    Cython implementation of _StringView

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1StringView.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void StringView()
        """
        ...
    
    @overload
    def __init__(self, in_0: bytes ) -> None:
        """
        Cython signature: void StringView(const libcpp_string &)
        """
        ...
    
    @overload
    def __init__(self, in_0: StringView ) -> None:
        """
        Cython signature: void StringView(StringView &)
        """
        ...
    
    def substr(self, start: int , end: int ) -> StringView:
        """
        Cython signature: StringView substr(size_t start, size_t end)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ...
    
    def getString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getString()
        """
        ...
    
    def __richcmp__(self, other: StringView, op: int) -> Any:
        ... 


class TSE_Match:
    """
    Cython implementation of _TSE_Match

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TSE_Match.html>`_
    """
    
    spectrum: MSSpectrum
    
    score: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TSE_Match()
        """
        ...
    
    @overload
    def __init__(self, in_0: TSE_Match ) -> None:
        """
        Cython signature: void TSE_Match(TSE_Match &)
        """
        ...
    
    @overload
    def __init__(self, spectrum: MSSpectrum , score: float ) -> None:
        """
        Cython signature: void TSE_Match(MSSpectrum & spectrum, double score)
        """
        ... 


class TargetedSpectraExtractor:
    """
    Cython implementation of _TargetedSpectraExtractor

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TargetedSpectraExtractor.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TargetedSpectraExtractor()
        """
        ...
    
    @overload
    def __init__(self, in_0: TargetedSpectraExtractor ) -> None:
        """
        Cython signature: void TargetedSpectraExtractor(TargetedSpectraExtractor &)
        """
        ...
    
    def getDefaultParameters(self, in_0: Param ) -> None:
        """
        Cython signature: void getDefaultParameters(Param &)
        """
        ...
    
    @overload
    def annotateSpectra(self, in_0: List[MSSpectrum] , in_1: TargetedExperiment , in_2: List[MSSpectrum] , in_3: FeatureMap ) -> None:
        """
        Cython signature: void annotateSpectra(libcpp_vector[MSSpectrum] &, TargetedExperiment &, libcpp_vector[MSSpectrum] &, FeatureMap &)
        """
        ...
    
    @overload
    def annotateSpectra(self, in_0: List[MSSpectrum] , in_1: TargetedExperiment , in_2: List[MSSpectrum] ) -> None:
        """
        Cython signature: void annotateSpectra(libcpp_vector[MSSpectrum] &, TargetedExperiment &, libcpp_vector[MSSpectrum] &)
        """
        ...
    
    @overload
    def annotateSpectra(self, in_0: List[MSSpectrum] , in_1: FeatureMap , in_2: FeatureMap , in_3: List[MSSpectrum] ) -> None:
        """
        Cython signature: void annotateSpectra(libcpp_vector[MSSpectrum] &, FeatureMap &, FeatureMap &, libcpp_vector[MSSpectrum] &)
        """
        ...
    
    def searchSpectrum(self, in_0: FeatureMap , in_1: FeatureMap , in_2: bool ) -> None:
        """
        Cython signature: void searchSpectrum(FeatureMap &, FeatureMap &, bool)
        """
        ...
    
    def pickSpectrum(self, in_0: MSSpectrum , in_1: MSSpectrum ) -> None:
        """
        Cython signature: void pickSpectrum(MSSpectrum &, MSSpectrum &)
        """
        ...
    
    @overload
    def scoreSpectra(self, in_0: List[MSSpectrum] , in_1: List[MSSpectrum] , in_2: FeatureMap , in_3: List[MSSpectrum] ) -> None:
        """
        Cython signature: void scoreSpectra(libcpp_vector[MSSpectrum] &, libcpp_vector[MSSpectrum] &, FeatureMap &, libcpp_vector[MSSpectrum] &)
        """
        ...
    
    @overload
    def scoreSpectra(self, in_0: List[MSSpectrum] , in_1: List[MSSpectrum] , in_2: List[MSSpectrum] ) -> None:
        """
        Cython signature: void scoreSpectra(libcpp_vector[MSSpectrum] &, libcpp_vector[MSSpectrum] &, libcpp_vector[MSSpectrum] &)
        """
        ...
    
    @overload
    def selectSpectra(self, in_0: List[MSSpectrum] , in_1: FeatureMap , in_2: List[MSSpectrum] , in_3: FeatureMap ) -> None:
        """
        Cython signature: void selectSpectra(libcpp_vector[MSSpectrum] &, FeatureMap &, libcpp_vector[MSSpectrum] &, FeatureMap &)
        """
        ...
    
    @overload
    def selectSpectra(self, in_0: List[MSSpectrum] , in_1: List[MSSpectrum] ) -> None:
        """
        Cython signature: void selectSpectra(libcpp_vector[MSSpectrum] &, libcpp_vector[MSSpectrum] &)
        """
        ...
    
    @overload
    def extractSpectra(self, in_0: MSExperiment , in_1: TargetedExperiment , in_2: List[MSSpectrum] , in_3: FeatureMap , in_4: bool ) -> None:
        """
        Cython signature: void extractSpectra(MSExperiment &, TargetedExperiment &, libcpp_vector[MSSpectrum] &, FeatureMap &, bool)
        """
        ...
    
    @overload
    def extractSpectra(self, in_0: MSExperiment , in_1: TargetedExperiment , in_2: List[MSSpectrum] ) -> None:
        """
        Cython signature: void extractSpectra(MSExperiment &, TargetedExperiment &, libcpp_vector[MSSpectrum] &)
        """
        ...
    
    @overload
    def extractSpectra(self, in_0: MSExperiment , in_1: FeatureMap , in_2: List[MSSpectrum] ) -> None:
        """
        Cython signature: void extractSpectra(MSExperiment &, FeatureMap &, libcpp_vector[MSSpectrum] &)
        """
        ...
    
    def constructTransitionsList(self, in_0: FeatureMap , in_1: FeatureMap , in_2: TargetedExperiment ) -> None:
        """
        Cython signature: void constructTransitionsList(FeatureMap &, FeatureMap &, TargetedExperiment &)
        """
        ...
    
    def storeSpectraMSP(self, in_0: Union[bytes, str, String] , in_1: MSExperiment ) -> None:
        """
        Cython signature: void storeSpectraMSP(const String &, MSExperiment &)
        """
        ...
    
    def mergeFeatures(self, in_0: FeatureMap , in_1: FeatureMap ) -> None:
        """
        Cython signature: void mergeFeatures(FeatureMap &, FeatureMap &)
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


class ThresholdMower:
    """
    Cython implementation of _ThresholdMower

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ThresholdMower.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ThresholdMower()
        """
        ...
    
    @overload
    def __init__(self, in_0: ThresholdMower ) -> None:
        """
        Cython signature: void ThresholdMower(ThresholdMower &)
        """
        ...
    
    def filterSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterSpectrum(MSSpectrum & spec)
        """
        ...
    
    def filterPeakSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterPeakSpectrum(MSSpectrum & spec)
        """
        ...
    
    def filterPeakMap(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void filterPeakMap(MSExperiment & exp)
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


class TraMLFile:
    """
    Cython implementation of _TraMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TraMLFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TraMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: TraMLFile ) -> None:
        """
        Cython signature: void TraMLFile(TraMLFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , id: TargetedExperiment ) -> None:
        """
        Cython signature: void load(String filename, TargetedExperiment & id)
        Loads a map from a TraML file
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , id: TargetedExperiment ) -> None:
        """
        Cython signature: void store(String filename, TargetedExperiment & id)
        Stores a map in a TraML file
        """
        ...
    
    def isSemanticallyValid(self, filename: Union[bytes, str, String] , errors: List[bytes] , warnings: List[bytes] ) -> bool:
        """
        Cython signature: bool isSemanticallyValid(String filename, StringList & errors, StringList & warnings)
        Checks if a file is valid with respect to the mapping file and the controlled vocabulary
        
        :param filename: File name of the file to be checked
        :param errors: Errors during the validation are returned in this output parameter
        :param warnings: Warnings during the validation are returned in this output parameter
        """
        ... 


class UnimodXMLFile:
    """
    Cython implementation of _UnimodXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1UnimodXMLFile.html>`_
      -- Inherits from ['XMLFile']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void UnimodXMLFile()
        """
        ...
    
    def getVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVersion()
        Return the version of the schema
        """
        ... 


class __AcquisitionMode:
    None
    ACQMODENULL : int
    PULSECOUNTING : int
    ADC : int
    TDC : int
    TRANSIENTRECORDER : int
    SIZE_OF_ACQUISITIONMODE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class DriftTimeUnit:
    None
    NONE : int
    MILLISECOND : int
    VSSC : int
    FAIMS_COMPENSATION_VOLTAGE : int
    SIZE_OF_DRIFTTIMEUNIT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class IMFormat:
    None
    NONE : int
    CONCATENATED : int
    MULTIPLE_SPECTRA : int
    MIXED : int
    SIZE_OF_IMFORMAT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class ITRAQ_TYPES:
    None
    FOURPLEX : int
    EIGHTPLEX : int
    TMT_SIXPLEX : int
    SIZE_OF_ITRAQ_TYPES : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class Measure:
    None
    MEASURE_PPM : int
    MEASURE_DA : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class NormalizationMethod:
    None
    NM_SCALE : int
    NM_SHIFT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __NumpressCompression:
    None
    NONE : int
    LINEAR : int
    PIC : int
    SLOF : int
    SIZE_OF_NUMPRESSCOMPRESSION : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class OriginAnnotationFormat:
    None
    FILE_ORIGIN : int
    MAP_INDEX : int
    ID_MERGE_INDEX : int
    UNKNOWN_OAF : int
    SIZE_OF_ORIGIN_ANNOTATION_FORMAT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __RETURN_STATUS:
    None
    SOLVED : int
    ITERATION_EXCEEDED : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class TermSpecificityNuc:
    None
    ANYWHERE : int
    FIVE_PRIME : int
    THREE_PRIME : int
    NUMBER_OF_TERM_SPECIFICITY : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __Type_IonDetector:
    None
    TYPENULL : int
    ELECTRONMULTIPLIER : int
    PHOTOMULTIPLIER : int
    FOCALPLANEARRAY : int
    FARADAYCUP : int
    CONVERSIONDYNODEELECTRONMULTIPLIER : int
    CONVERSIONDYNODEPHOTOMULTIPLIER : int
    MULTICOLLECTOR : int
    CHANNELELECTRONMULTIPLIER : int
    CHANNELTRON : int
    DALYDETECTOR : int
    MICROCHANNELPLATEDETECTOR : int
    ARRAYDETECTOR : int
    CONVERSIONDYNODE : int
    DYNODE : int
    FOCALPLANECOLLECTOR : int
    IONTOPHOTONDETECTOR : int
    POINTCOLLECTOR : int
    POSTACCELERATIONDETECTOR : int
    PHOTODIODEARRAYDETECTOR : int
    INDUCTIVEDETECTOR : int
    ELECTRONMULTIPLIERTUBE : int
    SIZE_OF_TYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 

