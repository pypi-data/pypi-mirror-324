from __future__ import annotations
from typing import overload, Any, List, Dict, Tuple, Set, Sequence, Union
from pyopenms import *  # pylint: disable=wildcard-import; lgtm(py/polluting-import)
import numpy as _np

from enum import Enum as _PyEnum


def __static_IonIdentityMolecularNetworking_annotateConsensusMap(consensus_map: ConsensusMap ) -> None:
    """
    Cython signature: void annotateConsensusMap(ConsensusMap & consensus_map)
        Annotate ConsensusMap for ion identity molecular networking (IIMN) workflow by GNPS.
        
        Adds meta values Constants::UserParams::IIMN_ROW_ID (unique index for each feature), Constants::UserParams::IIMN_ADDUCT_PARTNERS (related features row IDs)
        and Constants::UserParams::IIMN_ANNOTATION_NETWORK_NUMBER (all related features with different adduct states) get the same network number).
        This method requires the features annotated with the Constants::UserParams::IIMN_LINKED_GROUPS meta value.
        If at least one of the features has an annotation for Constants::UserParam::IIMN_LINKED_GROUPS, annotate ConsensusMap for IIMN.
        
        
        :param consensus_map: Input ConsensusMap without IIMN annotations.
    """
    ...

def __static_MRMRTNormalizer_chauvenet(residuals: List[float] , pos: int ) -> bool:
    """
    Cython signature: bool chauvenet(libcpp_vector[double] residuals, int pos)
    """
    ...

def __static_MRMRTNormalizer_chauvenet_probability(residuals: List[float] , pos: int ) -> float:
    """
    Cython signature: double chauvenet_probability(libcpp_vector[double] residuals, int pos)
    """
    ...

def __static_MRMRTNormalizer_computeBinnedCoverage(rtRange: List[float, float] , pairs: List[List[float, float]] , nrBins: int , minPeptidesPerBin: int , minBinsFilled: int ) -> bool:
    """
    Cython signature: bool computeBinnedCoverage(libcpp_pair[double,double] rtRange, libcpp_vector[libcpp_pair[double,double]] & pairs, int nrBins, int minPeptidesPerBin, int minBinsFilled)
    """
    ...

def __static_FileHandler_computeFileHash(filename: Union[bytes, str, String] ) -> Union[bytes, str, String]:
    """
    Cython signature: String computeFileHash(const String & filename)
    """
    ...

def __static_PrecursorCorrection_correctToHighestIntensityMS1Peak(exp: MSExperiment , mz_tolerance: float , ppm: bool , delta_mzs: List[float] , mzs: List[float] , rts: List[float] ) -> Set[int]:
    """
    Cython signature: libcpp_set[size_t] correctToHighestIntensityMS1Peak(MSExperiment & exp, double mz_tolerance, bool ppm, libcpp_vector[double] & delta_mzs, libcpp_vector[double] & mzs, libcpp_vector[double] & rts)
    """
    ...

def __static_PrecursorCorrection_correctToNearestFeature(features: FeatureMap , exp: MSExperiment , rt_tolerance_s: float , mz_tolerance: float , ppm: bool , believe_charge: bool , keep_original: bool , all_matching_features: bool , max_trace: int , debug_level: int ) -> Set[int]:
    """
    Cython signature: libcpp_set[size_t] correctToNearestFeature(FeatureMap & features, MSExperiment & exp, double rt_tolerance_s, double mz_tolerance, bool ppm, bool believe_charge, bool keep_original, bool all_matching_features, int max_trace, int debug_level)
    """
    ...

def __static_PrecursorCorrection_correctToNearestMS1Peak(exp: MSExperiment , mz_tolerance: float , ppm: bool , delta_mzs: List[float] , mzs: List[float] , rts: List[float] ) -> Set[int]:
    """
    Cython signature: libcpp_set[size_t] correctToNearestMS1Peak(MSExperiment & exp, double mz_tolerance, bool ppm, libcpp_vector[double] & delta_mzs, libcpp_vector[double] & mzs, libcpp_vector[double] & rts)
    """
    ...

def __static_CalibrationData_getMetaValues() -> List[bytes]:
    """
    Cython signature: StringList getMetaValues()
    """
    ...

def __static_PrecursorCorrection_getPrecursors(exp: MSExperiment , precursors: List[Precursor] , precursors_rt: List[float] , precursor_scan_index: List[int] ) -> None:
    """
    Cython signature: void getPrecursors(MSExperiment & exp, libcpp_vector[Precursor] & precursors, libcpp_vector[double] & precursors_rt, libcpp_vector[size_t] & precursor_scan_index)
    """
    ...

def __static_FileHandler_getType(filename: Union[bytes, str, String] ) -> int:
    """
    Cython signature: int getType(const String & filename)
    """
    ...

def __static_FileHandler_getTypeByContent(filename: Union[bytes, str, String] ) -> int:
    """
    Cython signature: FileType getTypeByContent(const String & filename)
    """
    ...

def __static_FileHandler_getTypeByFileName(filename: Union[bytes, str, String] ) -> int:
    """
    Cython signature: FileType getTypeByFileName(const String & filename)
    """
    ...

def __static_FileHandler_hasValidExtension(filename: Union[bytes, str, String] , type_: int ) -> bool:
    """
    Cython signature: bool hasValidExtension(const String & filename, FileType type_)
    """
    ...

def __static_FileHandler_isSupported(type_: int ) -> bool:
    """
    Cython signature: bool isSupported(FileType type_)
    """
    ...

def __static_MRMRTNormalizer_removeOutliersIterative(pairs: List[List[float, float]] , rsq_limit: float , coverage_limit: float , use_chauvenet: bool , outlier_detection_method: bytes ) -> List[List[float, float]]:
    """
    Cython signature: libcpp_vector[libcpp_pair[double,double]] removeOutliersIterative(libcpp_vector[libcpp_pair[double,double]] & pairs, double rsq_limit, double coverage_limit, bool use_chauvenet, libcpp_string outlier_detection_method)
    """
    ...

def __static_MRMRTNormalizer_removeOutliersRANSAC(pairs: List[List[float, float]] , rsq_limit: float , coverage_limit: float , max_iterations: int , max_rt_threshold: float , sampling_size: int ) -> List[List[float, float]]:
    """
    Cython signature: libcpp_vector[libcpp_pair[double,double]] removeOutliersRANSAC(libcpp_vector[libcpp_pair[double,double]] & pairs, double rsq_limit, double coverage_limit, size_t max_iterations, double max_rt_threshold, size_t sampling_size)
    """
    ...

def __static_SpectrumHelper_removePeaks(p: MSChromatogram , pos_start: float , pos_end: float ) -> None:
    """
    Cython signature: void removePeaks(MSChromatogram & p, double pos_start, double pos_end)
    """
    ...

def __static_SpectrumHelper_removePeaks(p: MSSpectrum , pos_start: float , pos_end: float ) -> None:
    """
    Cython signature: void removePeaks(MSSpectrum & p, double pos_start, double pos_end)
    """
    ...

def __static_FileHandler_stripExtension(file: Union[bytes, str, String] ) -> Union[bytes, str, String]:
    """
    Cython signature: String stripExtension(String file)
    """
    ...

def __static_SpectrumHelper_subtractMinimumIntensity(p: MSChromatogram ) -> None:
    """
    Cython signature: void subtractMinimumIntensity(MSChromatogram & p)
    """
    ...

def __static_SpectrumHelper_subtractMinimumIntensity(p: MSSpectrum ) -> None:
    """
    Cython signature: void subtractMinimumIntensity(MSSpectrum & p)
    """
    ...

def __static_FileHandler_swapExtension(filename: Union[bytes, str, String] , new_type: int ) -> Union[bytes, str, String]:
    """
    Cython signature: String swapExtension(String filename, FileType new_type)
    """
    ...

def __static_PrecursorCorrection_writeHist(out_csv: String , delta_mzs: List[float] , mzs: List[float] , rts: List[float] ) -> None:
    """
    Cython signature: void writeHist(String & out_csv, libcpp_vector[double] & delta_mzs, libcpp_vector[double] & mzs, libcpp_vector[double] & rts)
    """
    ...

def __static_IonIdentityMolecularNetworking_writeSupplementaryPairTable(consensus_map: ConsensusMap , output_file: Union[bytes, str, String] ) -> None:
    """
    Cython signature: void writeSupplementaryPairTable(const ConsensusMap & consensus_map, const String & output_file)
        Write supplementary pair table (csv file) from a ConsensusMap with edge annotations for connected features. Required for GNPS IIMN.
        
        The table contains the columns "ID 1" (row ID of first feature), "ID 2" (row ID of second feature), "EdgeType" (MS1/2 annotation),
        "Score" (the number of direct partners from both connected features) and "Annotation" (adducts and delta m/z between two connected features).
        
        
        :param consensus_map: Input ConsensusMap annotated with IonIdentityMolecularNetworking.annotateConsensusMap.
        :param output_file: Output file path for the supplementary pair table.
    """
    ...


class AAIndex:
    """
    Cython implementation of _AAIndex

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AAIndex.html>`_
    """
    
    def aliphatic(self, aa: bytes ) -> float:
        """
        Cython signature: double aliphatic(char aa)
        """
        ...
    
    def acidic(self, aa: bytes ) -> float:
        """
        Cython signature: double acidic(char aa)
        """
        ...
    
    def basic(self, aa: bytes ) -> float:
        """
        Cython signature: double basic(char aa)
        """
        ...
    
    def polar(self, aa: bytes ) -> float:
        """
        Cython signature: double polar(char aa)
        """
        ...
    
    def getKHAG800101(self, aa: bytes ) -> float:
        """
        Cython signature: double getKHAG800101(char aa)
        """
        ...
    
    def getVASM830103(self, aa: bytes ) -> float:
        """
        Cython signature: double getVASM830103(char aa)
        """
        ...
    
    def getNADH010106(self, aa: bytes ) -> float:
        """
        Cython signature: double getNADH010106(char aa)
        """
        ...
    
    def getNADH010107(self, aa: bytes ) -> float:
        """
        Cython signature: double getNADH010107(char aa)
        """
        ...
    
    def getWILM950102(self, aa: bytes ) -> float:
        """
        Cython signature: double getWILM950102(char aa)
        """
        ...
    
    def getROBB760107(self, aa: bytes ) -> float:
        """
        Cython signature: double getROBB760107(char aa)
        """
        ...
    
    def getOOBM850104(self, aa: bytes ) -> float:
        """
        Cython signature: double getOOBM850104(char aa)
        """
        ...
    
    def getFAUJ880111(self, aa: bytes ) -> float:
        """
        Cython signature: double getFAUJ880111(char aa)
        """
        ...
    
    def getFINA770101(self, aa: bytes ) -> float:
        """
        Cython signature: double getFINA770101(char aa)
        """
        ...
    
    def getARGP820102(self, aa: bytes ) -> float:
        """
        Cython signature: double getARGP820102(char aa)
        """
        ...
    
    def calculateGB(self, seq: AASequence , T: float ) -> float:
        """
        Cython signature: double calculateGB(AASequence & seq, double T)
        """
        ... 


class AbsoluteQuantitationStandardsFile:
    """
    Cython implementation of _AbsoluteQuantitationStandardsFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AbsoluteQuantitationStandardsFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AbsoluteQuantitationStandardsFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: AbsoluteQuantitationStandardsFile ) -> None:
        """
        Cython signature: void AbsoluteQuantitationStandardsFile(AbsoluteQuantitationStandardsFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , run_concentrations: List[AQS_runConcentration] ) -> None:
        """
        Cython signature: void load(const String & filename, libcpp_vector[AQS_runConcentration] & run_concentrations)
        """
        ... 


class BSpline2d:
    """
    Cython implementation of _BSpline2d

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1BSpline2d.html>`_
    """
    
    def __init__(self, x: List[float] , y: List[float] , wave_length: float , boundary_condition: int , num_nodes: int ) -> None:
        """
        Cython signature: void BSpline2d(libcpp_vector[double] x, libcpp_vector[double] y, double wave_length, BoundaryCondition boundary_condition, size_t num_nodes)
        """
        ...
    
    def solve(self, y: List[float] ) -> bool:
        """
        Cython signature: bool solve(libcpp_vector[double] y)
        Solve the spline curve for a new set of y values. Returns false if the solution fails
        """
        ...
    
    def eval(self, x: float ) -> float:
        """
        Cython signature: double eval(double x)
        Returns the evaluation of the smoothed curve at a particular x value. If current state is not ok(), returns zero
        """
        ...
    
    def derivative(self, x: float ) -> float:
        """
        Cython signature: double derivative(double x)
        Returns the first derivative of the spline curve at the given position x. Returns zero if the current state is not ok()
        """
        ...
    
    def ok(self) -> bool:
        """
        Cython signature: bool ok()
        Returns whether the spline fit was successful
        """
        ...
    
    def debug(self, enable: bool ) -> None:
        """
        Cython signature: void debug(bool enable)
        Enable or disable debug messages from the B-spline library
        """
        ... 


class CalibrationData:
    """
    Cython implementation of _CalibrationData

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CalibrationData.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CalibrationData()
        """
        ...
    
    @overload
    def __init__(self, in_0: CalibrationData ) -> None:
        """
        Cython signature: void CalibrationData(CalibrationData &)
        """
        ...
    
    def getMZ(self, in_0: int ) -> float:
        """
        Cython signature: double getMZ(size_t)
        Retrieve the observed m/z of the i'th calibration point
        """
        ...
    
    def getRT(self, in_0: int ) -> float:
        """
        Cython signature: double getRT(size_t)
        Retrieve the observed RT of the i'th calibration point
        """
        ...
    
    def getIntensity(self, in_0: int ) -> float:
        """
        Cython signature: double getIntensity(size_t)
        Retrieve the intensity of the i'th calibration point
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        Number of calibration points
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        Returns `True` if there are no peaks
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        Remove all calibration points
        """
        ...
    
    def setUsePPM(self, in_0: bool ) -> None:
        """
        Cython signature: void setUsePPM(bool)
        """
        ...
    
    def usePPM(self) -> bool:
        """
        Cython signature: bool usePPM()
        Current error unit (ppm or Th)
        """
        ...
    
    def insertCalibrationPoint(self, rt: float , mz_obs: float , intensity: float , mz_ref: float , weight: float , group: int ) -> None:
        """
        Cython signature: void insertCalibrationPoint(double rt, double mz_obs, float intensity, double mz_ref, double weight, int group)
        """
        ...
    
    def getNrOfGroups(self) -> int:
        """
        Cython signature: size_t getNrOfGroups()
        Number of peak groups (can be 0)
        """
        ...
    
    def getError(self, in_0: int ) -> float:
        """
        Cython signature: double getError(size_t)
        Retrieve the error for i'th calibrant in either ppm or Th (depending on usePPM())
        """
        ...
    
    def getRefMZ(self, in_0: int ) -> float:
        """
        Cython signature: double getRefMZ(size_t)
        Retrieve the theoretical m/z of the i'th calibration point
        """
        ...
    
    def getWeight(self, in_0: int ) -> float:
        """
        Cython signature: double getWeight(size_t)
        Retrieve the weight of the i'th calibration point
        """
        ...
    
    def getGroup(self, i: int ) -> int:
        """
        Cython signature: int getGroup(size_t i)
        Retrieve the group of the i'th calibration point
        """
        ...
    
    def median(self, in_0: float , in_1: float ) -> CalibrationData:
        """
        Cython signature: CalibrationData median(double, double)
        Compute the median in the given RT range for every peak group
        """
        ...
    
    def sortByRT(self) -> None:
        """
        Cython signature: void sortByRT()
        Sort calibration points by RT, to allow for valid RT chunking
        """
        ...
    
    getMetaValues: __static_CalibrationData_getMetaValues 


class DigestionEnzyme:
    """
    Cython implementation of _DigestionEnzyme

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DigestionEnzyme.html>`_

      Base class for digestion enzymes
    """
    
    @overload
    def __init__(self, in_0: DigestionEnzyme ) -> None:
        """
        Cython signature: void DigestionEnzyme(DigestionEnzyme &)
        """
        ...
    
    @overload
    def __init__(self, name: Union[bytes, str, String] , cleavage_regex: Union[bytes, str, String] , synonyms: Set[bytes] , regex_description: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void DigestionEnzyme(const String & name, const String & cleavage_regex, libcpp_set[String] & synonyms, String regex_description)
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
    
    def __richcmp__(self, other: DigestionEnzyme, op: int) -> Any:
        ... 


class EDTAFile:
    """
    Cython implementation of _EDTAFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1EDTAFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void EDTAFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: EDTAFile ) -> None:
        """
        Cython signature: void EDTAFile(EDTAFile &)
        """
        ...
    
    @overload
    def store(self, filename: Union[bytes, str, String] , map: FeatureMap ) -> None:
        """
        Cython signature: void store(String filename, FeatureMap & map)
        """
        ...
    
    @overload
    def store(self, filename: Union[bytes, str, String] , map: ConsensusMap ) -> None:
        """
        Cython signature: void store(String filename, ConsensusMap & map)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , consensus_map: ConsensusMap ) -> None:
        """
        Cython signature: void load(String filename, ConsensusMap & consensus_map)
        """
        ... 


class EmgScoring:
    """
    Cython implementation of _EmgScoring

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1EmgScoring.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void EmgScoring()
        Helps in scoring of an elution peak using an exponentially modified gaussian distribution model
        """
        ...
    
    @overload
    def __init__(self, in_0: EmgScoring ) -> None:
        """
        Cython signature: void EmgScoring(EmgScoring &)
        """
        ...
    
    def setFitterParam(self, param: Param ) -> None:
        """
        Cython signature: void setFitterParam(Param param)
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        """
        ...
    
    def elutionModelFit(self, current_section: '_np.ndarray[Any, _np.dtype[_np.float32]]' , smooth_data: bool ) -> float:
        """
        Cython signature: double elutionModelFit(libcpp_vector[DPosition2] current_section, bool smooth_data)
        """
        ... 


class EnzymaticDigestion:
    """
    Cython implementation of _EnzymaticDigestion

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1EnzymaticDigestion.html>`_

      Class for the enzymatic digestion of proteins
    
      Digestion can be performed using simple regular expressions, e.g. [KR] | [^P] for trypsin.
      Also missed cleavages can be modeled, i.e. adjacent peptides are not cleaved
      due to enzyme malfunction/access restrictions. If n missed cleavages are allowed, all possible resulting
      peptides (cleaved and uncleaved) with up to n missed cleavages are returned.
      Thus no random selection of just n specific missed cleavage sites is performed.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void EnzymaticDigestion()
        """
        ...
    
    @overload
    def __init__(self, in_0: EnzymaticDigestion ) -> None:
        """
        Cython signature: void EnzymaticDigestion(EnzymaticDigestion &)
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
    
    def setEnzyme(self, enzyme: DigestionEnzyme ) -> None:
        """
        Cython signature: void setEnzyme(DigestionEnzyme * enzyme)
        Sets the enzyme for the digestion
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
    Specificity : __Specificity 


class FeatureGroupingAlgorithmKD:
    """
    Cython implementation of _FeatureGroupingAlgorithmKD

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureGroupingAlgorithmKD.html>`_
      -- Inherits from ['FeatureGroupingAlgorithm', 'ProgressLogger']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureGroupingAlgorithmKD()
        A feature grouping algorithm for unlabeled data
        """
        ...
    
    @overload
    def group(self, maps: List[FeatureMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void group(libcpp_vector[FeatureMap] & maps, ConsensusMap & out)
        """
        ...
    
    @overload
    def group(self, maps: List[ConsensusMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void group(libcpp_vector[ConsensusMap] & maps, ConsensusMap & out)
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


class FileHandler:
    """
    Cython implementation of _FileHandler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FileHandler.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FileHandler()
        """
        ...
    
    def loadExperiment(self, in_0: Union[bytes, str, String] , in_1: MSExperiment ) -> None:
        """
        Cython signature: void loadExperiment(String, MSExperiment &)
        Loads a file into an MSExperiment
        
        
        :param filename: The file name of the file to load
        :param exp: The experiment to load the data into
        :param force_type: Forces to load the file with that file type. If no type is forced, it is determined from the extension (or from the content if that fails)
        :param log: Progress logging mode
        :param rewrite_source_file: Set's the SourceFile name and path to the current file. Note that this looses the link to the primary MS run the file originated from
        :param compute_hash: If source files are rewritten, this flag triggers a recomputation of hash values. A SHA1 string gets stored in the checksum member of SourceFile
        :return: true if the file could be loaded, false otherwise
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ...
    
    def storeExperiment(self, in_0: Union[bytes, str, String] , in_1: MSExperiment ) -> None:
        """
        Cython signature: void storeExperiment(String, MSExperiment)
        Stores an MSExperiment to a file\n
        
        The file type to store the data in is determined by the file name. Supported formats for storing are mzML, mzXML, mzData and DTA2D. If the file format cannot be determined from the file name, the mzML format is used
        
        
        :param filename: The name of the file to store the data in
        :param exp: The experiment to store
        :param log: Progress logging mode
        :raises:
          Exception: UnableToCreateFile is thrown if the file could not be written
        """
        ...
    
    def loadFeatures(self, in_0: Union[bytes, str, String] , in_1: FeatureMap ) -> None:
        """
        Cython signature: void loadFeatures(String, FeatureMap &)
        Loads a file into a FeatureMap
        
        
        :param filename: The file name of the file to load
        :param map: The FeatureMap to load the data into
        :param force_type: Forces to load the file with that file type. If no type is forced, it is determined from the extension (or from the content if that fails)
        :return: true if the file could be loaded, false otherwise
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ...
    
    def getOptions(self) -> PeakFileOptions:
        """
        Cython signature: PeakFileOptions getOptions()
        Access to the options for loading/storing
        """
        ...
    
    def setOptions(self, in_0: PeakFileOptions ) -> None:
        """
        Cython signature: void setOptions(PeakFileOptions)
        Sets options for loading/storing
        """
        ...
    
    computeFileHash: __static_FileHandler_computeFileHash
    
    getType: __static_FileHandler_getType
    
    getTypeByContent: __static_FileHandler_getTypeByContent
    
    getTypeByFileName: __static_FileHandler_getTypeByFileName
    
    hasValidExtension: __static_FileHandler_hasValidExtension
    
    isSupported: __static_FileHandler_isSupported
    
    stripExtension: __static_FileHandler_stripExtension
    
    swapExtension: __static_FileHandler_swapExtension 


class FileTypes:
    """
    Cython implementation of _FileTypes

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FileTypes.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FileTypes()
        Centralizes the file types recognized by FileHandler
        """
        ...
    
    @overload
    def __init__(self, in_0: FileTypes ) -> None:
        """
        Cython signature: void FileTypes(FileTypes &)
        """
        ...
    
    def typeToName(self, t: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String typeToName(FileType t)
        Returns the name/extension of the type
        """
        ...
    
    def typeToMZML(self, t: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String typeToMZML(FileType t)
        Returns the mzML name
        """
        ...
    
    def nameToType(self, name: Union[bytes, str, String] ) -> int:
        """
        Cython signature: FileType nameToType(String name)
        Converts a file type name into a Type
        
        
        :param name: A case-insensitive name (e.g. FASTA or Fasta, etc.)
        """
        ... 


class HyperScore:
    """
    Cython implementation of _HyperScore

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1HyperScore.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void HyperScore()
        An implementation of the X!Tandem HyperScore PSM scoring function
        """
        ...
    
    @overload
    def __init__(self, in_0: HyperScore ) -> None:
        """
        Cython signature: void HyperScore(HyperScore &)
        """
        ...
    
    def compute(self, fragment_mass_tolerance: float , fragment_mass_tolerance_unit_ppm: bool , exp_spectrum: MSSpectrum , theo_spectrum: MSSpectrum ) -> float:
        """
        Cython signature: double compute(double fragment_mass_tolerance, bool fragment_mass_tolerance_unit_ppm, MSSpectrum & exp_spectrum, MSSpectrum & theo_spectrum)
        Compute the (ln transformed) X!Tandem HyperScore\n
        
        1. the dot product of peak intensities between matching peaks in experimental and theoretical spectrum is calculated
        2. the HyperScore is calculated from the dot product by multiplying by factorials of matching b- and y-ions
        
        
        :note: Peak intensities of the theoretical spectrum are typically 1 or TIC normalized, but can also be e.g. ion probabilities
        :param fragment_mass_tolerance: Mass tolerance applied left and right of the theoretical spectrum peak position
        :param fragment_mass_tolerance_unit_ppm: Unit of the mass tolerance is: Thomson if false, ppm if true
        :param exp_spectrum: Measured spectrum
        :param theo_spectrum: Theoretical spectrum Peaks need to contain an ion annotation as provided by TheoreticalSpectrumGenerator
        """
        ... 


class IMSElement:
    """
    Cython implementation of _IMSElement

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ims::IMSElement_1_1IMSElement.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IMSElement()
        Represents a chemical atom with name and isotope distribution
        """
        ...
    
    @overload
    def __init__(self, in_0: IMSElement ) -> None:
        """
        Cython signature: void IMSElement(IMSElement &)
        """
        ...
    
    @overload
    def __init__(self, name: bytes , isotopes: IMSIsotopeDistribution ) -> None:
        """
        Cython signature: void IMSElement(libcpp_string & name, IMSIsotopeDistribution & isotopes)
        """
        ...
    
    @overload
    def __init__(self, name: bytes , mass: float ) -> None:
        """
        Cython signature: void IMSElement(libcpp_string & name, double mass)
        """
        ...
    
    @overload
    def __init__(self, name: bytes , nominal_mass: int ) -> None:
        """
        Cython signature: void IMSElement(libcpp_string & name, unsigned int nominal_mass)
        """
        ...
    
    def getName(self) -> bytes:
        """
        Cython signature: libcpp_string getName()
        Gets element's name
        """
        ...
    
    def setName(self, name: bytes ) -> None:
        """
        Cython signature: void setName(libcpp_string & name)
        Sets element's name
        """
        ...
    
    def getSequence(self) -> bytes:
        """
        Cython signature: libcpp_string getSequence()
        Gets element's sequence
        """
        ...
    
    def setSequence(self, sequence: bytes ) -> None:
        """
        Cython signature: void setSequence(libcpp_string & sequence)
        Sets element's sequence
        """
        ...
    
    def getNominalMass(self) -> int:
        """
        Cython signature: unsigned int getNominalMass()
        Gets element's nominal mass
        """
        ...
    
    def getMass(self, index: int ) -> float:
        """
        Cython signature: double getMass(int index)
        Gets mass of element's isotope 'index'
        """
        ...
    
    def getAverageMass(self) -> float:
        """
        Cython signature: double getAverageMass()
        Gets element's average mass
        """
        ...
    
    def getIonMass(self, electrons_number: int ) -> float:
        """
        Cython signature: double getIonMass(int electrons_number)
        Gets ion mass of element. By default ion lacks 1 electron, but this can be changed by setting other 'electrons_number'
        """
        ...
    
    def getIsotopeDistribution(self) -> IMSIsotopeDistribution:
        """
        Cython signature: IMSIsotopeDistribution getIsotopeDistribution()
        Gets element's isotope distribution
        """
        ...
    
    def setIsotopeDistribution(self, isotopes: IMSIsotopeDistribution ) -> None:
        """
        Cython signature: void setIsotopeDistribution(IMSIsotopeDistribution & isotopes)
        Sets element's isotope distribution
        """
        ...
    
    def __richcmp__(self, other: IMSElement, op: int) -> Any:
        ... 


class IMSWeights:
    """
    Cython implementation of _IMSWeights

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ims::Weights_1_1IMSWeights.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IMSWeights()
        """
        ...
    
    @overload
    def __init__(self, in_0: IMSWeights ) -> None:
        """
        Cython signature: void IMSWeights(IMSWeights)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: int size()
        Gets size of a set of weights
        """
        ...
    
    def getWeight(self, i: int ) -> int:
        """
        Cython signature: unsigned long int getWeight(int i)
        Gets a scaled integer weight by index
        """
        ...
    
    def setPrecision(self, precision: float ) -> None:
        """
        Cython signature: void setPrecision(double precision)
        Sets a new precision to scale double values to integer
        """
        ...
    
    def getPrecision(self) -> float:
        """
        Cython signature: double getPrecision()
        Gets precision.
        """
        ...
    
    def back(self) -> int:
        """
        Cython signature: unsigned long int back()
        Gets a last weight
        """
        ...
    
    def getAlphabetMass(self, i: int ) -> float:
        """
        Cython signature: double getAlphabetMass(int i)
        Gets an original (double) alphabet mass by index
        """
        ...
    
    def getParentMass(self, decomposition: List[int] ) -> float:
        """
        Cython signature: double getParentMass(libcpp_vector[unsigned int] & decomposition)
        Returns a parent mass for a given `decomposition`
        """
        ...
    
    def swap(self, index1: int , index2: int ) -> None:
        """
        Cython signature: void swap(int index1, int index2)
        Exchanges weight and mass at index1 with weight and mass at index2
        """
        ...
    
    def divideByGCD(self) -> bool:
        """
        Cython signature: bool divideByGCD()
        Divides the integer weights by their gcd. The precision is also adjusted
        """
        ...
    
    def getMinRoundingError(self) -> float:
        """
        Cython signature: double getMinRoundingError()
        """
        ...
    
    def getMaxRoundingError(self) -> float:
        """
        Cython signature: double getMaxRoundingError()
        """
        ... 


class IndexedMzMLFileLoader:
    """
    Cython implementation of _IndexedMzMLFileLoader

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IndexedMzMLFileLoader.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void IndexedMzMLFileLoader()
        A class to load an indexedmzML file
        """
        ...
    
    def load(self, in_0: Union[bytes, str, String] , in_1: OnDiscMSExperiment ) -> bool:
        """
        Cython signature: bool load(String, OnDiscMSExperiment &)
        Load a file\n
        
        Tries to parse the file, success needs to be checked with the return value
        """
        ...
    
    @overload
    def store(self, in_0: Union[bytes, str, String] , in_1: OnDiscMSExperiment ) -> None:
        """
        Cython signature: void store(String, OnDiscMSExperiment &)
        Store a file from an on-disc data-structure
        
        
        :param filename: Filename determines where the file will be stored
        :param exp: MS data to be stored
        """
        ...
    
    @overload
    def store(self, in_0: Union[bytes, str, String] , in_1: MSExperiment ) -> None:
        """
        Cython signature: void store(String, MSExperiment &)
        Store a file from an in-memory data-structure
        
        
        :param filename: Filename determines where the file will be stored
        :param exp: MS data to be stored
        """
        ...
    
    def getOptions(self) -> PeakFileOptions:
        """
        Cython signature: PeakFileOptions getOptions()
        Returns the options for loading/storing
        """
        ...
    
    def setOptions(self, in_0: PeakFileOptions ) -> None:
        """
        Cython signature: void setOptions(PeakFileOptions)
        Returns the options for loading/storing
        """
        ... 


class InterpolationModel:
    """
    Cython implementation of _InterpolationModel

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1InterpolationModel.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void InterpolationModel()
        Abstract class for 1D-models that are approximated using linear interpolation
        """
        ...
    
    @overload
    def __init__(self, in_0: InterpolationModel ) -> None:
        """
        Cython signature: void InterpolationModel(InterpolationModel &)
        """
        ...
    
    def getIntensity(self, coord: float ) -> float:
        """
        Cython signature: double getIntensity(double coord)
        Access model predicted intensity at position 'pos'
        """
        ...
    
    def getScalingFactor(self) -> float:
        """
        Cython signature: double getScalingFactor()
        Returns the interpolation class
        """
        ...
    
    def setOffset(self, offset: float ) -> None:
        """
        Cython signature: void setOffset(double offset)
        Sets the offset of the model
        """
        ...
    
    def getCenter(self) -> float:
        """
        Cython signature: double getCenter()
        Returns the "center" of the model, particular definition (depends on the derived model)
        """
        ...
    
    def setSamples(self) -> None:
        """
        Cython signature: void setSamples()
        Sets sample/supporting points of interpolation wrt params
        """
        ...
    
    def setInterpolationStep(self, interpolation_step: float ) -> None:
        """
        Cython signature: void setInterpolationStep(double interpolation_step)
        Sets the interpolation step for the linear interpolation of the model
        """
        ...
    
    def setScalingFactor(self, scaling: float ) -> None:
        """
        Cython signature: void setScalingFactor(double scaling)
        Sets the scaling factor of the model
        """
        ...
    
    def getInterpolation(self) -> LinearInterpolation:
        """
        Cython signature: LinearInterpolation getInterpolation()
        Returns the interpolation class
        """
        ... 


class IonIdentityMolecularNetworking:
    """
    Cython implementation of _IonIdentityMolecularNetworking

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IonIdentityMolecularNetworking.html>`_

    Includes the necessary functions to generate filed required for GNPS ion identity molecular networking (IIMN).
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void IonIdentityMolecularNetworking()
        """
        ...
    
    annotateConsensusMap: __static_IonIdentityMolecularNetworking_annotateConsensusMap
    
    writeSupplementaryPairTable: __static_IonIdentityMolecularNetworking_writeSupplementaryPairTable 


class IonSource:
    """
    Cython implementation of _IonSource

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IonSource.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IonSource()
        Description of an ion source (part of a MS Instrument)
        """
        ...
    
    @overload
    def __init__(self, in_0: IonSource ) -> None:
        """
        Cython signature: void IonSource(IonSource &)
        """
        ...
    
    def getPolarity(self) -> int:
        """
        Cython signature: Polarity getPolarity()
        Returns the ionization mode
        """
        ...
    
    def setPolarity(self, polarity: int ) -> None:
        """
        Cython signature: void setPolarity(Polarity polarity)
        Sets the ionization mode
        """
        ...
    
    def getInletType(self) -> int:
        """
        Cython signature: InletType getInletType()
        Returns the inlet type
        """
        ...
    
    def setInletType(self, inlet_type: int ) -> None:
        """
        Cython signature: void setInletType(InletType inlet_type)
        Sets the inlet type
        """
        ...
    
    def getIonizationMethod(self) -> int:
        """
        Cython signature: IonizationMethod getIonizationMethod()
        Returns the ionization method
        """
        ...
    
    def setIonizationMethod(self, ionization_type: int ) -> None:
        """
        Cython signature: void setIonizationMethod(IonizationMethod ionization_type)
        Sets the ionization method
        """
        ...
    
    def getOrder(self) -> int:
        """
        Cython signature: int getOrder()
        Returns the position of this part in the whole Instrument
        
        Order can be ignored, as long the instrument has this default setup:
          - one ion source
          - one or many mass analyzers
          - one ion detector
        
        For more complex instruments, the order should be defined.
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
    
    def __richcmp__(self, other: IonSource, op: int) -> Any:
        ...
    InletType : __InletType
    IonizationMethod : __IonizationMethod
    Polarity : __Polarity 


class ItraqFourPlexQuantitationMethod:
    """
    Cython implementation of _ItraqFourPlexQuantitationMethod

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ItraqFourPlexQuantitationMethod.html>`_
      -- Inherits from ['IsobaricQuantitationMethod']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ItraqFourPlexQuantitationMethod()
        iTRAQ 4 plex quantitation to be used with the IsobaricQuantitation
        """
        ...
    
    @overload
    def __init__(self, in_0: ItraqFourPlexQuantitationMethod ) -> None:
        """
        Cython signature: void ItraqFourPlexQuantitationMethod(ItraqFourPlexQuantitationMethod &)
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


class LinearResampler:
    """
    Cython implementation of _LinearResampler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1LinearResampler.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LinearResampler()
        """
        ...
    
    @overload
    def __init__(self, in_0: LinearResampler ) -> None:
        """
        Cython signature: void LinearResampler(LinearResampler &)
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


class MRMMapping:
    """
    Cython implementation of _MRMMapping

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMMapping.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void MRMMapping()
        """
        ...
    
    def mapExperiment(self, input_chromatograms: MSExperiment , targeted_exp: TargetedExperiment , output: MSExperiment ) -> None:
        """
        Cython signature: void mapExperiment(MSExperiment input_chromatograms, TargetedExperiment targeted_exp, MSExperiment & output)
        Maps input chromatograms to assays in a targeted experiment
        
        The output chromatograms are an annotated copy of the input chromatograms
        with native id, precursor information and peptide sequence (if available)
        annotated in the chromatogram files
        
        The algorithm tries to match a given set of chromatograms and targeted
        assays. It iterates through all the chromatograms retrieves one or more
        matching targeted assay for the chromatogram. By default, the algorithm
        assumes that a 1:1 mapping exists. If a chromatogram cannot be mapped
        (does not have a corresponding assay) the algorithm issues a warning, the
        user can specify that the program should abort in such a case (see
        error_on_unmapped)
        
        :note If multiple mapping is enabled (see map_multiple_assays parameter)
        then each mapped assay will get its own chromatogram that contains the
        same raw data but different meta-annotation. This *can* be useful if the
        same transition is used to monitor multiple analytes but may also
        indicate a problem with too wide mapping tolerances
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


class MRMRTNormalizer:
    """
    Cython implementation of _MRMRTNormalizer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMRTNormalizer.html>`_
    """
    
    chauvenet: __static_MRMRTNormalizer_chauvenet
    
    chauvenet_probability: __static_MRMRTNormalizer_chauvenet_probability
    
    computeBinnedCoverage: __static_MRMRTNormalizer_computeBinnedCoverage
    
    removeOutliersIterative: __static_MRMRTNormalizer_removeOutliersIterative
    
    removeOutliersRANSAC: __static_MRMRTNormalizer_removeOutliersRANSAC 


class MRMScoring:
    """
    Cython implementation of _MRMScoring

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1MRMScoring.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMScoring()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMScoring ) -> None:
        """
        Cython signature: void MRMScoring(MRMScoring &)
        """
        ...
    
    def calcXcorrCoelutionScore(self) -> float:
        """
        Cython signature: double calcXcorrCoelutionScore()
        Calculate the cross-correlation coelution score. The score is a distance where zero indicates perfect coelution
        """
        ...
    
    def calcXcorrCoelutionWeightedScore(self, normalized_library_intensity: List[float] ) -> float:
        """
        Cython signature: double calcXcorrCoelutionWeightedScore(libcpp_vector[double] & normalized_library_intensity)
        Calculate the weighted cross-correlation coelution score
        
        The score is a distance where zero indicates perfect coelution. The
        score is weighted by the transition intensities, non-perfect coelution
        in low-intensity transitions should thus become less important
        """
        ...
    
    def calcSeparateXcorrContrastCoelutionScore(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] calcSeparateXcorrContrastCoelutionScore()
        Calculate the separate cross-correlation contrast score
        """
        ...
    
    def calcXcorrPrecursorContrastCoelutionScore(self) -> float:
        """
        Cython signature: double calcXcorrPrecursorContrastCoelutionScore()
        Calculate the precursor cross-correlation contrast score against the transitions
        
        The score is a distance where zero indicates perfect coelution
        """
        ...
    
    def calcXcorrShapeScore(self) -> float:
        """
        Cython signature: double calcXcorrShapeScore()
        Calculate the cross-correlation shape score
        
        The score is a correlation measure where 1 indicates perfect correlation
        and 0 means no correlation.
        """
        ...
    
    def calcXcorrShapeWeightedScore(self, normalized_library_intensity: List[float] ) -> float:
        """
        Cython signature: double calcXcorrShapeWeightedScore(libcpp_vector[double] & normalized_library_intensity)
        Calculate the weighted cross-correlation shape score
        
        The score is a correlation measure where 1 indicates perfect correlation
        and 0 means no correlation. The score is weighted by the transition
        intensities, non-perfect coelution in low-intensity transitions should
        thus become less important
        """
        ...
    
    def calcSeparateXcorrContrastShapeScore(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] calcSeparateXcorrContrastShapeScore()
        Calculate the separate cross-correlation contrast shape score
        """
        ...
    
    def calcXcorrPrecursorContrastShapeScore(self) -> float:
        """
        Cython signature: double calcXcorrPrecursorContrastShapeScore()
        Calculate the precursor cross-correlation shape score against the transitions
        """
        ...
    
    def calcRTScore(self, peptide: LightCompound , normalized_experimental_rt: float ) -> float:
        """
        Cython signature: double calcRTScore(LightCompound & peptide, double normalized_experimental_rt)
        """
        ...
    
    def calcMIScore(self) -> float:
        """
        Cython signature: double calcMIScore()
        """
        ...
    
    def calcMIWeightedScore(self, normalized_library_intensity: List[float] ) -> float:
        """
        Cython signature: double calcMIWeightedScore(const libcpp_vector[double] & normalized_library_intensity)
        """
        ...
    
    def calcMIPrecursorScore(self) -> float:
        """
        Cython signature: double calcMIPrecursorScore()
        """
        ...
    
    def calcMIPrecursorContrastScore(self) -> float:
        """
        Cython signature: double calcMIPrecursorContrastScore()
        """
        ...
    
    def calcMIPrecursorCombinedScore(self) -> float:
        """
        Cython signature: double calcMIPrecursorCombinedScore()
        """
        ...
    
    def calcSeparateMIContrastScore(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] calcSeparateMIContrastScore()
        """
        ...
    
    def getMIMatrix(self) -> MatrixDouble:
        """
        Cython signature: MatrixDouble getMIMatrix()
        """
        ... 


class MSDataSqlConsumer:
    """
    Cython implementation of _MSDataSqlConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSDataSqlConsumer.html>`_
    """
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] , run_id: int , buffer_size: int , full_meta: bool , lossy_compression: bool , linear_mass_acc: float ) -> None:
        """
        Cython signature: void MSDataSqlConsumer(String filename, uint64_t run_id, int buffer_size, bool full_meta, bool lossy_compression, double linear_mass_acc)
        """
        ...
    
    @overload
    def __init__(self, in_0: MSDataSqlConsumer ) -> None:
        """
        Cython signature: void MSDataSqlConsumer(MSDataSqlConsumer &)
        """
        ...
    
    def flush(self) -> None:
        """
        Cython signature: void flush()
        Flushes the data for good
        
        After calling this function, no more data is held in the buffer but the
        class is still able to receive new data
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        Write a spectrum to the output file
        """
        ...
    
    def consumeChromatogram(self, c: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram & c)
        Write a chromatogram to the output file
        """
        ...
    
    def setExpectedSize(self, expectedSpectra: int , expectedChromatograms: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t expectedSpectra, size_t expectedChromatograms)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings & exp)
        """
        ... 


class MSDataStoringConsumer:
    """
    Cython implementation of _MSDataStoringConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSDataStoringConsumer.html>`_

    Consumer class that simply stores the data
    
    This class is able to keep spectra and chromatograms passed to it in memory
    and the data can be accessed through getData()
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MSDataStoringConsumer()
        """
        ...
    
    @overload
    def __init__(self, in_0: MSDataStoringConsumer ) -> None:
        """
        Cython signature: void MSDataStoringConsumer(MSDataStoringConsumer &)
        """
        ...
    
    def setExperimentalSettings(self, exp: ExperimentalSettings ) -> None:
        """
        Cython signature: void setExperimentalSettings(ExperimentalSettings & exp)
        Sets experimental settings
        """
        ...
    
    def setExpectedSize(self, expectedSpectra: int , expectedChromatograms: int ) -> None:
        """
        Cython signature: void setExpectedSize(size_t expectedSpectra, size_t expectedChromatograms)
        Sets expected size
        """
        ...
    
    def consumeSpectrum(self, s: MSSpectrum ) -> None:
        """
        Cython signature: void consumeSpectrum(MSSpectrum & s)
        """
        ...
    
    def consumeChromatogram(self, in_0: MSChromatogram ) -> None:
        """
        Cython signature: void consumeChromatogram(MSChromatogram &)
        """
        ...
    
    def getData(self) -> MSExperiment:
        """
        Cython signature: MSExperiment getData()
        """
        ... 


class MSPFile:
    """
    Cython implementation of _MSPFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSPFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MSPFile()
        File adapter for MSP files (NIST spectra library)
        """
        ...
    
    @overload
    def __init__(self, in_0: MSPFile ) -> None:
        """
        Cython signature: void MSPFile(MSPFile &)
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , exp: MSExperiment ) -> None:
        """
        Cython signature: void store(String filename, MSExperiment & exp)
        Stores a map in a MSPFile file
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , ids: List[PeptideIdentification] , exp: MSExperiment ) -> None:
        """
        Cython signature: void load(String filename, libcpp_vector[PeptideIdentification] & ids, MSExperiment & exp)
        Loads a map from a MSPFile file
        
        
        :param exp: PeakMap which contains the spectra after reading
        :param filename: The filename of the experiment
        :param ids: Output parameter which contains the peptide identifications from the spectra annotations
        """
        ... 


class MSPGenericFile:
    """
    Cython implementation of _MSPGenericFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSPGenericFile.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MSPGenericFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MSPGenericFile ) -> None:
        """
        Cython signature: void MSPGenericFile(MSPGenericFile &)
        """
        ...
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] , library: MSExperiment ) -> None:
        """
        Cython signature: void MSPGenericFile(const String & filename, MSExperiment & library)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , library: MSExperiment ) -> None:
        """
        Cython signature: void load(const String & filename, MSExperiment & library)
        Load the file's data and metadata, and save it into an `MSExperiment`
        
        
        :param filename: Path to the MSP input file
        :param library: The variable into which the extracted information will be saved
        :raises:
          Exception: FileNotFound If the file could not be found
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , library: MSExperiment ) -> None:
        """
        Cython signature: void store(const String & filename, const MSExperiment & library)
        Save data and metadata into a file
        
        
        :param filename: Path to the MSP input file
        :param library: The variable from which extracted information will be saved
        :raises:
          Exception: FileNotWritable If the file is not writable
        """
        ...
    
    def getDefaultParameters(self, params: Param ) -> None:
        """
        Cython signature: void getDefaultParameters(Param & params)
        Returns the class' default parameters
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


class MapAlignmentEvaluationAlgorithmRecall:
    """
    Cython implementation of _MapAlignmentEvaluationAlgorithmRecall

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MapAlignmentEvaluationAlgorithmRecall.html>`_
      -- Inherits from ['MapAlignmentEvaluationAlgorithm']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void MapAlignmentEvaluationAlgorithmRecall()
        """
        ... 


class MassExplainer:
    """
    Cython implementation of _MassExplainer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MassExplainer.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MassExplainer()
        Computes empirical formulas for given mass differences using a set of allowed elements
        """
        ...
    
    @overload
    def __init__(self, in_0: MassExplainer ) -> None:
        """
        Cython signature: void MassExplainer(MassExplainer &)
        """
        ...
    
    @overload
    def __init__(self, adduct_base: List[Adduct] ) -> None:
        """
        Cython signature: void MassExplainer(libcpp_vector[Adduct] adduct_base)
        """
        ...
    
    @overload
    def __init__(self, q_min: int , q_max: int , max_span: int , thresh_logp: float ) -> None:
        """
        Cython signature: void MassExplainer(int q_min, int q_max, int max_span, double thresh_logp)
        """
        ...
    
    def setAdductBase(self, adduct_base: List[Adduct] ) -> None:
        """
        Cython signature: void setAdductBase(libcpp_vector[Adduct] adduct_base)
        Sets the set of possible adducts
        """
        ...
    
    def getAdductBase(self) -> List[Adduct]:
        """
        Cython signature: libcpp_vector[Adduct] getAdductBase()
        Returns the set of adducts
        """
        ...
    
    def getCompomerById(self, id: int ) -> Compomer:
        """
        Cython signature: Compomer getCompomerById(size_t id)
        Returns a compomer by its Id (useful after a query() )
        """
        ...
    
    def compute(self) -> None:
        """
        Cython signature: void compute()
        Fill map with possible mass-differences along with their explanation
        """
        ... 


class MatrixDouble:
    """
    Cython implementation of _Matrix[double]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Matrix[double].html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MatrixDouble()
        """
        ...
    
    @overload
    def __init__(self, in_0: MatrixDouble ) -> None:
        """
        Cython signature: void MatrixDouble(MatrixDouble)
        """
        ...
    
    @overload
    def __init__(self, rows: int , cols: int , value: float ) -> None:
        """
        Cython signature: void MatrixDouble(size_t rows, size_t cols, double value)
        """
        ...
    
    def getValue(self, i: int , j: int ) -> float:
        """
        Cython signature: double getValue(size_t i, size_t j)
        """
        ...
    
    def setValue(self, i: int , j: int , value: float ) -> None:
        """
        Cython signature: void setValue(size_t i, size_t j, double value)
        """
        ...
    
    def rows(self) -> int:
        """
        Cython signature: size_t rows()
        """
        ...
    
    def cols(self) -> int:
        """
        Cython signature: size_t cols()
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ...
    
    def resize(self, rows: int , cols: int ) -> None:
        """
        Cython signature: void resize(size_t rows, size_t cols)
        """
        ... 


class MetaboTargetedAssay:
    """
    Cython implementation of _MetaboTargetedAssay

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaboTargetedAssay.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaboTargetedAssay()
        This class provides methods for the extraction of targeted assays for metabolomics
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaboTargetedAssay ) -> None:
        """
        Cython signature: void MetaboTargetedAssay(MetaboTargetedAssay &)
        """
        ...
    
    def extractMetaboTargetedAssay(self, spectra: MSExperiment , feature_ms2_index: FeatureMapping_FeatureToMs2Indices , precursor_rt_tol: float , precursor_mz_distance: float , cosine_sim_threshold: float , transition_threshold: float , min_fragment_mz: float , max_fragment_mz: float , method_consensus_spectrum: bool , exclude_ms2_precursor: bool , file_counter: int ) -> List[MetaboTargetedAssay]:
        """
        Cython signature: libcpp_vector[MetaboTargetedAssay] extractMetaboTargetedAssay(MSExperiment & spectra, FeatureMapping_FeatureToMs2Indices & feature_ms2_index, double & precursor_rt_tol, double & precursor_mz_distance, double & cosine_sim_threshold, double & transition_threshold, double & min_fragment_mz, double & max_fragment_mz, bool & method_consensus_spectrum, bool & exclude_ms2_precursor, unsigned int & file_counter)
        Extract a vector of MetaboTargetedAssays without using fragment annotation
        
        
        :param spectra: Input of MSExperiment with spectra information
        :param feature_ms2_spectra_map: FeatureMapping class with associated MS2 spectra
        :param precursor_rt_tol: Retention time tolerance of the precursor
        :param precursor_mz_distance: Max m/z distance of the precursor entries of two spectra to be merged
        :param cosine_sim_threshold: Cosine similarty threshold for the usage of SpectraMerger
        :param transition_threshold: Intensity threshold for MS2 peak used in MetaboTargetedAssay
        :param min_fragment_mz: Minimum m/z a fragment ion has to have to be considered as a transition
        :param max_fragment_mz: Maximum m/z a fragment ion has to have to be considered as a transition
        :param method_consensus_spectrum: Boolean to use consensus spectrum method
        :param exclude_ms2_precursor: Boolean to exclude MS2 precursor from MetaboTargetedAssay
        :return: Vector of MetaboTargetedAssay
        """
        ...
    
    def extractMetaboTargetedAssayFragmentAnnotation(self, v_cmp_spec: List[MetaboTargetedAssay_CompoundTargetDecoyPair] , transition_threshold: float , min_fragment_mz: float , max_fragment_mz: float , use_exact_mass: bool , exclude_ms2_precursor: bool ) -> List[MetaboTargetedAssay]:
        """
        Cython signature: libcpp_vector[MetaboTargetedAssay] extractMetaboTargetedAssayFragmentAnnotation(libcpp_vector[MetaboTargetedAssay_CompoundTargetDecoyPair] & v_cmp_spec, double & transition_threshold, double & min_fragment_mz, double & max_fragment_mz, bool & use_exact_mass, bool & exclude_ms2_precursor)
        Extract a vector of MetaboTargetedAssays using fragment
        
        
        :param v_cmp_spec: Vector of CompoundInfo with associated fragment annotated MSspectrum
        :param transition_threshold: Intensity threshold for MS2 peak used in MetaboTargetedAssay
        :param min_fragment_mz: Minimum m/z a fragment ion has to have to be considered as a transition
        :param max_fragment_mz: Maximum m/z a fragment ion has to have to be considered as a transition
        :param use_exact_mass: Boolean if exact mass should be used as peak mass for annotated fragments
        :param exclude_ms2_precursor: Boolean to exclude MS2 precursor from MetaboTargetedAssay
        :param file_counter: Count if multiple files are used.
        :return: Vector of MetaboTargetedAssay
        """
        ...
    
    def pairCompoundWithAnnotatedTDSpectraPairs(self, v_cmpinfo: List[SiriusMSFile_CompoundInfo] , annotated_spectra: List[SiriusFragmentAnnotation_SiriusTargetDecoySpectra] ) -> List[MetaboTargetedAssay_CompoundTargetDecoyPair]:
        """
        Cython signature: libcpp_vector[MetaboTargetedAssay_CompoundTargetDecoyPair] pairCompoundWithAnnotatedTDSpectraPairs(libcpp_vector[SiriusMSFile_CompoundInfo] & v_cmpinfo, libcpp_vector[SiriusFragmentAnnotation_SiriusTargetDecoySpectra] & annotated_spectra)
        Pair compound information (SiriusMSFile) with the annotated target and decoy spectrum from SIRIUS/Passatutto based on the m_id (unique identifier composed of description_filepath_native_id_k introduced in the SiriusMSConverter)
        
        
        :param v_cmpinfo: Vector of SiriusMSFile::CompoundInfo
        :param annotated_spectra: Vector of SiriusTargetDecoySpectra
        :return: Vector of MetaboTargetedAssay::CompoundTargetDecoyPair
        """
        ... 


class MetaboTargetedAssay_CompoundTargetDecoyPair:
    """
    Cython implementation of _MetaboTargetedAssay_CompoundTargetDecoyPair

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaboTargetedAssay_CompoundTargetDecoyPair.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaboTargetedAssay_CompoundTargetDecoyPair()
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaboTargetedAssay_CompoundTargetDecoyPair ) -> None:
        """
        Cython signature: void MetaboTargetedAssay_CompoundTargetDecoyPair(MetaboTargetedAssay_CompoundTargetDecoyPair &)
        """
        ... 


class MzMLSpectrumDecoder:
    """
    Cython implementation of _MzMLSpectrumDecoder

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzMLSpectrumDecoder.html>`_

    A class to decode input strings that contain an mzML chromatogram or spectrum tag
    
    It uses xercesc to parse a string containing either a exactly one mzML
    spectrum or chromatogram (from <chromatogram> to </chromatogram> or
    <spectrum> to </spectrum> tag). It returns the data contained in the
    binaryDataArray for Intensity / mass-to-charge or Intensity / time
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzMLSpectrumDecoder()
        """
        ...
    
    @overload
    def __init__(self, in_0: MzMLSpectrumDecoder ) -> None:
        """
        Cython signature: void MzMLSpectrumDecoder(MzMLSpectrumDecoder &)
        """
        ...
    
    def domParseChromatogram(self, in_: Union[bytes, str, String] , cptr: _Interfaces_Chromatogram ) -> None:
        """
        Cython signature: void domParseChromatogram(String in_, shared_ptr[_Interfaces_Chromatogram] & cptr)
        Extract data from a string which contains a full mzML chromatogram
        
        Extracts data from the input string which is expected to contain exactly
        one <chromatogram> tag (from <chromatogram> to </chromatogram>). This
        function will extract the contained binaryDataArray and provide the
        result as Chromatogram
        
        
        :param in: Input string containing the raw XML
        :param cptr: Resulting chromatogram
        """
        ...
    
    def domParseSpectrum(self, in_: Union[bytes, str, String] , cptr: _Interfaces_Spectrum ) -> None:
        """
        Cython signature: void domParseSpectrum(String in_, shared_ptr[_Interfaces_Spectrum] & cptr)
        Extract data from a string which contains a full mzML spectrum
        
        Extracts data from the input string which is expected to contain exactly
        one <spectrum> tag (from <spectrum> to </spectrum>). This function will
        extract the contained binaryDataArray and provide the result as Spectrum
        
        
        :param in: Input string containing the raw XML
        :param cptr: Resulting spectrum
        """
        ...
    
    def setSkipXMLChecks(self, only: bool ) -> None:
        """
        Cython signature: void setSkipXMLChecks(bool only)
        Whether to skip some XML checks (e.g. removing whitespace inside base64 arrays) and be fast instead
        """
        ... 


class MzXMLFile:
    """
    Cython implementation of _MzXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzXMLFile.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzXMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MzXMLFile ) -> None:
        """
        Cython signature: void MzXMLFile(MzXMLFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , exp: MSExperiment ) -> None:
        """
        Cython signature: void load(String filename, MSExperiment & exp)
        Loads a MSExperiment from a MzXML file
        
        
        :param exp: MSExperiment
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , exp: MSExperiment ) -> None:
        """
        Cython signature: void store(String filename, MSExperiment & exp)
        Stores a MSExperiment in a MzXML file
        
        
        :param exp: MSExperiment
        """
        ...
    
    def getOptions(self) -> PeakFileOptions:
        """
        Cython signature: PeakFileOptions getOptions()
        Returns the options for loading/storing
        """
        ...
    
    def setOptions(self, in_0: PeakFileOptions ) -> None:
        """
        Cython signature: void setOptions(PeakFileOptions)
        Sets options for loading/storing
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


class OPXLHelper:
    """
    Cython implementation of _OPXLHelper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OPXLHelper.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OPXLHelper()
        """
        ...
    
    @overload
    def __init__(self, in_0: OPXLHelper ) -> None:
        """
        Cython signature: void OPXLHelper(OPXLHelper &)
        """
        ...
    
    def enumerateCrossLinksAndMasses(self, peptides: List[AASeqWithMass] , cross_link_mass_light: float , cross_link_mass_mono_link: List[float] , cross_link_residue1: List[bytes] , cross_link_residue2: List[bytes] , spectrum_precursors: List[float] , precursor_correction_positions: List[int] , precursor_mass_tolerance: float , precursor_mass_tolerance_unit_ppm: bool ) -> List[XLPrecursor]:
        """
        Cython signature: libcpp_vector[XLPrecursor] enumerateCrossLinksAndMasses(libcpp_vector[AASeqWithMass] peptides, double cross_link_mass_light, DoubleList cross_link_mass_mono_link, StringList cross_link_residue1, StringList cross_link_residue2, libcpp_vector[double] & spectrum_precursors, libcpp_vector[int] & precursor_correction_positions, double precursor_mass_tolerance, bool precursor_mass_tolerance_unit_ppm)
        """
        ...
    
    def digestDatabase(self, fasta_db: List[FASTAEntry] , digestor: EnzymaticDigestion , min_peptide_length: int , cross_link_residue1: List[bytes] , cross_link_residue2: List[bytes] , fixed_modifications: ModifiedPeptideGenerator_MapToResidueType , variable_modifications: ModifiedPeptideGenerator_MapToResidueType , max_variable_mods_per_peptide: int ) -> List[AASeqWithMass]:
        """
        Cython signature: libcpp_vector[AASeqWithMass] digestDatabase(libcpp_vector[FASTAEntry] fasta_db, EnzymaticDigestion digestor, size_t min_peptide_length, StringList cross_link_residue1, StringList cross_link_residue2, ModifiedPeptideGenerator_MapToResidueType & fixed_modifications, ModifiedPeptideGenerator_MapToResidueType & variable_modifications, size_t max_variable_mods_per_peptide)
        """
        ...
    
    def buildCandidates(self, candidates: List[XLPrecursor] , precursor_corrections: List[int] , precursor_correction_positions: List[int] , peptide_masses: List[AASeqWithMass] , cross_link_residue1: List[bytes] , cross_link_residue2: List[bytes] , cross_link_mass: float , cross_link_mass_mono_link: List[float] , spectrum_precursor_vector: List[float] , allowed_error_vector: List[float] , cross_link_name: Union[bytes, str, String] ) -> List[ProteinProteinCrossLink]:
        """
        Cython signature: libcpp_vector[ProteinProteinCrossLink] buildCandidates(libcpp_vector[XLPrecursor] & candidates, libcpp_vector[int] & precursor_corrections, libcpp_vector[int] & precursor_correction_positions, libcpp_vector[AASeqWithMass] & peptide_masses, const StringList & cross_link_residue1, const StringList & cross_link_residue2, double cross_link_mass, DoubleList cross_link_mass_mono_link, libcpp_vector[double] & spectrum_precursor_vector, libcpp_vector[double] & allowed_error_vector, String cross_link_name)
        """
        ...
    
    def buildFragmentAnnotations(self, frag_annotations: List[PeptideHit_PeakAnnotation] , matching: List[List[int, int]] , theoretical_spectrum: MSSpectrum , experiment_spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void buildFragmentAnnotations(libcpp_vector[PeptideHit_PeakAnnotation] & frag_annotations, libcpp_vector[libcpp_pair[size_t,size_t]] matching, MSSpectrum theoretical_spectrum, MSSpectrum experiment_spectrum)
        """
        ...
    
    def buildPeptideIDs(self, peptide_ids: List[PeptideIdentification] , top_csms_spectrum: List[CrossLinkSpectrumMatch] , all_top_csms: List[List[CrossLinkSpectrumMatch]] , all_top_csms_current_index: int , spectra: MSExperiment , scan_index: int , scan_index_heavy: int ) -> None:
        """
        Cython signature: void buildPeptideIDs(libcpp_vector[PeptideIdentification] & peptide_ids, libcpp_vector[CrossLinkSpectrumMatch] top_csms_spectrum, libcpp_vector[libcpp_vector[CrossLinkSpectrumMatch]] & all_top_csms, size_t all_top_csms_current_index, MSExperiment spectra, size_t scan_index, size_t scan_index_heavy)
        """
        ...
    
    def addProteinPositionMetaValues(self, peptide_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void addProteinPositionMetaValues(libcpp_vector[PeptideIdentification] & peptide_ids)
        """
        ...
    
    def addXLTargetDecoyMV(self, peptide_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void addXLTargetDecoyMV(libcpp_vector[PeptideIdentification] & peptide_ids)
        """
        ...
    
    def addBetaAccessions(self, peptide_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void addBetaAccessions(libcpp_vector[PeptideIdentification] & peptide_ids)
        """
        ...
    
    def removeBetaPeptideHits(self, peptide_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void removeBetaPeptideHits(libcpp_vector[PeptideIdentification] & peptide_ids)
        """
        ...
    
    def addPercolatorFeatureList(self, prot_id: ProteinIdentification ) -> None:
        """
        Cython signature: void addPercolatorFeatureList(ProteinIdentification & prot_id)
        """
        ...
    
    def computeDeltaScores(self, peptide_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void computeDeltaScores(libcpp_vector[PeptideIdentification] & peptide_ids)
        """
        ...
    
    def combineTopRanksFromPairs(self, peptide_ids: List[PeptideIdentification] , number_top_hits: int ) -> List[PeptideIdentification]:
        """
        Cython signature: libcpp_vector[PeptideIdentification] combineTopRanksFromPairs(libcpp_vector[PeptideIdentification] & peptide_ids, size_t number_top_hits)
        """
        ...
    
    def collectPrecursorCandidates(self, precursor_correction_steps: List[int] , precursor_mass: float , precursor_mass_tolerance: float , precursor_mass_tolerance_unit_ppm: bool , filtered_peptide_masses: List[AASeqWithMass] , cross_link_mass: float , cross_link_mass_mono_link: List[float] , cross_link_residue1: List[bytes] , cross_link_residue2: List[bytes] , cross_link_name: Union[bytes, str, String] , use_sequence_tags: bool , tags: List[Union[bytes, str]] ) -> List[ProteinProteinCrossLink]:
        """
        Cython signature: libcpp_vector[ProteinProteinCrossLink] collectPrecursorCandidates(IntList precursor_correction_steps, double precursor_mass, double precursor_mass_tolerance, bool precursor_mass_tolerance_unit_ppm, libcpp_vector[AASeqWithMass] filtered_peptide_masses, double cross_link_mass, DoubleList cross_link_mass_mono_link, StringList cross_link_residue1, StringList cross_link_residue2, String cross_link_name, bool use_sequence_tags, const libcpp_vector[libcpp_utf8_string] & tags)
        """
        ...
    
    def computePrecursorError(self, csm: CrossLinkSpectrumMatch , precursor_mz: float , precursor_charge: int ) -> float:
        """
        Cython signature: double computePrecursorError(CrossLinkSpectrumMatch csm, double precursor_mz, int precursor_charge)
        """
        ...
    
    def isoPeakMeans(self, csm: CrossLinkSpectrumMatch , num_iso_peaks_array: IntegerDataArray , matched_spec_linear_alpha: List[List[int, int]] , matched_spec_linear_beta: List[List[int, int]] , matched_spec_xlinks_alpha: List[List[int, int]] , matched_spec_xlinks_beta: List[List[int, int]] ) -> None:
        """
        Cython signature: void isoPeakMeans(CrossLinkSpectrumMatch & csm, IntegerDataArray & num_iso_peaks_array, libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_linear_alpha, libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_linear_beta, libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_xlinks_alpha, libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_xlinks_beta)
        """
        ... 


class OPXL_PreprocessedPairSpectra:
    """
    Cython implementation of _OPXL_PreprocessedPairSpectra

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::OPXLDataStructs_1_1OPXL_PreprocessedPairSpectra.html>`_
    """
    
    spectra_linear_peaks: MSExperiment
    
    spectra_xlink_peaks: MSExperiment
    
    spectra_all_peaks: MSExperiment
    
    @overload
    def __init__(self, size: int ) -> None:
        """
        Cython signature: void OPXL_PreprocessedPairSpectra(size_t size)
        """
        ...
    
    @overload
    def __init__(self, in_0: OPXL_PreprocessedPairSpectra ) -> None:
        """
        Cython signature: void OPXL_PreprocessedPairSpectra(OPXL_PreprocessedPairSpectra &)
        """
        ... 


class OSW_ChromExtractParams:
    """
    Cython implementation of _OSW_ChromExtractParams

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OSW_ChromExtractParams.html>`_
    """
    
    min_upper_edge_dist: float
    
    mz_extraction_window: float
    
    ppm: bool
    
    extraction_function: bytes
    
    rt_extraction_window: float
    
    extra_rt_extract: float
    
    im_extraction_window: float
    
    def __init__(self, in_0: OSW_ChromExtractParams ) -> None:
        """
        Cython signature: void OSW_ChromExtractParams(OSW_ChromExtractParams &)
        """
        ... 


class PeakTypeEstimator:
    """
    Cython implementation of _PeakTypeEstimator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeakTypeEstimator.html>`_

    Estimates if the data of a spectrum is raw data or peak data
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeakTypeEstimator()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeakTypeEstimator ) -> None:
        """
        Cython signature: void PeakTypeEstimator(PeakTypeEstimator &)
        """
        ... 


class PeptideAndProteinQuant:
    """
    Cython implementation of _PeptideAndProteinQuant

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeptideAndProteinQuant.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeptideAndProteinQuant()
        Helper class for peptide and protein quantification based on feature data annotated with IDs
        """
        ...
    
    @overload
    def __init__(self, in_0: PeptideAndProteinQuant ) -> None:
        """
        Cython signature: void PeptideAndProteinQuant(PeptideAndProteinQuant &)
        """
        ...
    
    @overload
    def readQuantData(self, map_in: FeatureMap , ed: ExperimentalDesign ) -> None:
        """
        Cython signature: void readQuantData(FeatureMap & map_in, ExperimentalDesign & ed)
        Read quantitative data from a feature map
        
        Parameters should be set before using this method, as setting parameters will clear all results
        """
        ...
    
    @overload
    def readQuantData(self, map_in: ConsensusMap , ed: ExperimentalDesign ) -> None:
        """
        Cython signature: void readQuantData(ConsensusMap & map_in, ExperimentalDesign & ed)
        Read quantitative data from a consensus map
        
        Parameters should be set before using this method, as setting parameters will clear all results
        """
        ...
    
    @overload
    def readQuantData(self, proteins: List[ProteinIdentification] , peptides: List[PeptideIdentification] , ed: ExperimentalDesign ) -> None:
        """
        Cython signature: void readQuantData(libcpp_vector[ProteinIdentification] & proteins, libcpp_vector[PeptideIdentification] & peptides, ExperimentalDesign & ed)
        Read quantitative data from identification results (for quantification via spectral counting)
        
        Parameters should be set before using this method, as setting parameters will clear all results
        """
        ...
    
    def quantifyPeptides(self, peptides: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void quantifyPeptides(libcpp_vector[PeptideIdentification] & peptides)
        Compute peptide abundances
        
        Based on quantitative data for individual charge states (in member `pep_quant_`), overall abundances for peptides are computed (and stored again in `pep_quant_`)
        Quantitative data must first be read via readQuantData()
        Optional (peptide-level) protein inference information (e.g. from Fido or ProteinProphet) can be supplied via `peptides`. In that case, peptide-to-protein associations - the basis for protein-level quantification - will also be read from `peptides`!
        """
        ...
    
    def quantifyProteins(self, proteins: ProteinIdentification ) -> None:
        """
        Cython signature: void quantifyProteins(ProteinIdentification & proteins)
        Compute protein abundances
        
        Peptide abundances must be computed first with quantifyPeptides(). Optional protein inference information (e.g. from Fido or ProteinProphet) can be supplied via `proteins`
        """
        ...
    
    def getStatistics(self) -> PeptideAndProteinQuant_Statistics:
        """
        Cython signature: PeptideAndProteinQuant_Statistics getStatistics()
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


class PeptideAndProteinQuant_PeptideData:
    """
    Cython implementation of _PeptideAndProteinQuant_PeptideData

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeptideAndProteinQuant_PeptideData.html>`_
    """
    
    accessions: Set[bytes]
    
    psm_count: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeptideAndProteinQuant_PeptideData()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeptideAndProteinQuant_PeptideData ) -> None:
        """
        Cython signature: void PeptideAndProteinQuant_PeptideData(PeptideAndProteinQuant_PeptideData &)
        """
        ... 


class PeptideAndProteinQuant_ProteinData:
    """
    Cython implementation of _PeptideAndProteinQuant_ProteinData

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeptideAndProteinQuant_ProteinData.html>`_
    """
    
    psm_count: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeptideAndProteinQuant_ProteinData()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeptideAndProteinQuant_ProteinData ) -> None:
        """
        Cython signature: void PeptideAndProteinQuant_ProteinData(PeptideAndProteinQuant_ProteinData &)
        """
        ... 


class PeptideAndProteinQuant_Statistics:
    """
    Cython implementation of _PeptideAndProteinQuant_Statistics

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeptideAndProteinQuant_Statistics.html>`_
    """
    
    n_samples: int
    
    quant_proteins: int
    
    too_few_peptides: int
    
    quant_peptides: int
    
    total_peptides: int
    
    quant_features: int
    
    total_features: int
    
    blank_features: int
    
    ambig_features: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeptideAndProteinQuant_Statistics()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeptideAndProteinQuant_Statistics ) -> None:
        """
        Cython signature: void PeptideAndProteinQuant_Statistics(PeptideAndProteinQuant_Statistics &)
        """
        ... 


class PosteriorErrorProbabilityModel:
    """
    Cython implementation of _PosteriorErrorProbabilityModel

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1PosteriorErrorProbabilityModel.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void PosteriorErrorProbabilityModel()
        """
        ...
    
    @overload
    def fit(self, search_engine_scores: List[float] , outlier_handling: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool fit(libcpp_vector[double] & search_engine_scores, String outlier_handling)
        Fits the distributions to the data points(search_engine_scores). Estimated parameters for the distributions are saved in member variables
        computeProbability can be used afterwards
        Uses two Gaussians to fit. And Gauss+Gauss or Gumbel+Gauss to plot and calculate final probabilities
        
        
        :param search_engine_scores: A vector which holds the data points
        :return: `true` if algorithm has run through. Else false will be returned. In that case no plot and no probabilities are calculated
        """
        ...
    
    @overload
    def fit(self, search_engine_scores: List[float] , probabilities: List[float] , outlier_handling: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool fit(libcpp_vector[double] & search_engine_scores, libcpp_vector[double] & probabilities, String outlier_handling)
        Fits the distributions to the data points(search_engine_scores). Estimated parameters for the distributions are saved in member variables
        computeProbability can be used afterwards
        Uses two Gaussians to fit. And Gauss+Gauss or Gumbel+Gauss to plot and calculate final probabilities
        
        
        :param search_engine_scores: A vector which holds the data points
        :param probabilities: A vector which holds the probability for each data point after running this function. If it has some content it will be overwritten
        :return: `true` if algorithm has run through. Else false will be returned. In that case no plot and no probabilities are calculated
        """
        ...
    
    def fillDensities(self, x_scores: List[float] , incorrect_density: List[float] , correct_density: List[float] ) -> None:
        """
        Cython signature: void fillDensities(libcpp_vector[double] & x_scores, libcpp_vector[double] & incorrect_density, libcpp_vector[double] & correct_density)
        Writes the distributions densities into the two vectors for a set of scores. Incorrect_densities represent the incorrectly assigned sequences
        """
        ...
    
    def fillLogDensities(self, x_scores: List[float] , incorrect_density: List[float] , correct_density: List[float] ) -> None:
        """
        Cython signature: void fillLogDensities(libcpp_vector[double] & x_scores, libcpp_vector[double] & incorrect_density, libcpp_vector[double] & correct_density)
        Writes the log distributions densities into the two vectors for a set of scores. Incorrect_densities represent the incorrectly assigned sequences
        """
        ...
    
    def computeLogLikelihood(self, incorrect_density: List[float] , correct_density: List[float] ) -> float:
        """
        Cython signature: double computeLogLikelihood(libcpp_vector[double] & incorrect_density, libcpp_vector[double] & correct_density)
        Computes the Maximum Likelihood with a log-likelihood function
        """
        ...
    
    def pos_neg_mean_weighted_posteriors(self, x_scores: List[float] , incorrect_posteriors: List[float] ) -> List[float, float]:
        """
        Cython signature: libcpp_pair[double,double] pos_neg_mean_weighted_posteriors(libcpp_vector[double] & x_scores, libcpp_vector[double] & incorrect_posteriors)
        """
        ...
    
    def getCorrectlyAssignedFitResult(self) -> GaussFitResult:
        """
        Cython signature: GaussFitResult getCorrectlyAssignedFitResult()
        Returns estimated parameters for correctly assigned sequences. Fit should be used before
        """
        ...
    
    def getIncorrectlyAssignedFitResult(self) -> GaussFitResult:
        """
        Cython signature: GaussFitResult getIncorrectlyAssignedFitResult()
        Returns estimated parameters for correctly assigned sequences. Fit should be used before
        """
        ...
    
    def getNegativePrior(self) -> float:
        """
        Cython signature: double getNegativePrior()
        Returns the estimated negative prior probability
        """
        ...
    
    def computeProbability(self, score: float ) -> float:
        """
        Cython signature: double computeProbability(double score)
        Returns the computed posterior error probability for a given score
        """
        ...
    
    def initPlots(self, x_scores: List[float] ) -> TextFile:
        """
        Cython signature: TextFile initPlots(libcpp_vector[double] & x_scores)
        Initializes the plots
        """
        ...
    
    def getGumbelGnuplotFormula(self, params: GaussFitResult ) -> Union[bytes, str, String]:
        """
        Cython signature: String getGumbelGnuplotFormula(GaussFitResult & params)
        Returns the gnuplot formula of the fitted gumbel distribution
        """
        ...
    
    def getGaussGnuplotFormula(self, params: GaussFitResult ) -> Union[bytes, str, String]:
        """
        Cython signature: String getGaussGnuplotFormula(GaussFitResult & params)
        Returns the gnuplot formula of the fitted gauss distribution
        """
        ...
    
    def getBothGnuplotFormula(self, incorrect: GaussFitResult , correct: GaussFitResult ) -> Union[bytes, str, String]:
        """
        Cython signature: String getBothGnuplotFormula(GaussFitResult & incorrect, GaussFitResult & correct)
        Returns the gnuplot formula of the fitted mixture distribution
        """
        ...
    
    def plotTargetDecoyEstimation(self, target: List[float] , decoy: List[float] ) -> None:
        """
        Cython signature: void plotTargetDecoyEstimation(libcpp_vector[double] & target, libcpp_vector[double] & decoy)
        Plots the estimated distribution against target and decoy hits
        """
        ...
    
    def getSmallestScore(self) -> float:
        """
        Cython signature: double getSmallestScore()
        Returns the smallest score used in the last fit
        """
        ...
    
    def tryGnuplot(self, gp_file: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void tryGnuplot(const String & gp_file)
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


class PrecursorCorrection:
    """
    Cython implementation of _PrecursorCorrection

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PrecursorCorrection.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PrecursorCorrection()
        """
        ...
    
    @overload
    def __init__(self, in_0: PrecursorCorrection ) -> None:
        """
        Cython signature: void PrecursorCorrection(PrecursorCorrection &)
        """
        ...
    
    correctToHighestIntensityMS1Peak: __static_PrecursorCorrection_correctToHighestIntensityMS1Peak
    
    correctToNearestFeature: __static_PrecursorCorrection_correctToNearestFeature
    
    correctToNearestMS1Peak: __static_PrecursorCorrection_correctToNearestMS1Peak
    
    getPrecursors: __static_PrecursorCorrection_getPrecursors
    
    writeHist: __static_PrecursorCorrection_writeHist 


class Product:
    """
    Cython implementation of _Product

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Product.html>`_

    This class describes the product isolation window for special scan types, such as MRM
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Product()
        """
        ...
    
    @overload
    def __init__(self, in_0: Product ) -> None:
        """
        Cython signature: void Product(Product &)
        """
        ...
    
    def getMZ(self) -> float:
        """
        Cython signature: double getMZ()
        Returns the target m/z
        """
        ...
    
    def setMZ(self, in_0: float ) -> None:
        """
        Cython signature: void setMZ(double)
        Sets the target m/z
        """
        ...
    
    def getIsolationWindowLowerOffset(self) -> float:
        """
        Cython signature: double getIsolationWindowLowerOffset()
        Returns the lower offset from the target m/z
        """
        ...
    
    def setIsolationWindowLowerOffset(self, bound: float ) -> None:
        """
        Cython signature: void setIsolationWindowLowerOffset(double bound)
        Sets the lower offset from the target m/z
        """
        ...
    
    def getIsolationWindowUpperOffset(self) -> float:
        """
        Cython signature: double getIsolationWindowUpperOffset()
        Returns the upper offset from the target m/z
        """
        ...
    
    def setIsolationWindowUpperOffset(self, bound: float ) -> None:
        """
        Cython signature: void setIsolationWindowUpperOffset(double bound)
        Sets the upper offset from the target m/z
        """
        ...
    
    def __richcmp__(self, other: Product, op: int) -> Any:
        ... 


class ProteinHit:
    """
    Cython implementation of _ProteinHit

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProteinHit.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProteinHit()
        """
        ...
    
    @overload
    def __init__(self, score: float , rank: int , accession: Union[bytes, str, String] , sequence: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void ProteinHit(double score, unsigned int rank, String accession, String sequence)
        """
        ...
    
    @overload
    def __init__(self, in_0: ProteinHit ) -> None:
        """
        Cython signature: void ProteinHit(ProteinHit &)
        """
        ...
    
    def getScore(self) -> float:
        """
        Cython signature: float getScore()
        Returns the score of the protein hit
        """
        ...
    
    def getRank(self) -> int:
        """
        Cython signature: unsigned int getRank()
        Returns the rank of the protein hit
        """
        ...
    
    def getSequence(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSequence()
        Returns the protein sequence
        """
        ...
    
    def getAccession(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getAccession()
        Returns the accession of the protein
        """
        ...
    
    def getDescription(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getDescription()
        Returns the description of the protein
        """
        ...
    
    def getCoverage(self) -> float:
        """
        Cython signature: double getCoverage()
        Returns the coverage (in percent) of the protein hit based upon matched peptides
        """
        ...
    
    def setScore(self, in_0: float ) -> None:
        """
        Cython signature: void setScore(float)
        Sets the score of the protein hit
        """
        ...
    
    def setRank(self, in_0: int ) -> None:
        """
        Cython signature: void setRank(unsigned int)
        Sets the rank
        """
        ...
    
    def setSequence(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSequence(String)
        Sets the protein sequence
        """
        ...
    
    def setAccession(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setAccession(String)
        Sets the accession of the protein
        """
        ...
    
    def setDescription(self, description: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setDescription(String description)
        Sets the description of the protein
        """
        ...
    
    def setCoverage(self, in_0: float ) -> None:
        """
        Cython signature: void setCoverage(double)
        Sets the coverage (in percent) of the protein hit based upon matched peptides
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
    
    def __richcmp__(self, other: ProteinHit, op: int) -> Any:
        ... 


class ProteinInference:
    """
    Cython implementation of _ProteinInference

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProteinInference.html>`_

    [experimental class] given a peptide quantitation, infer corresponding protein quantities
    
    Infers protein ratios from peptide ratios (currently using unique peptides only).
    Use the IDMapper class to add protein and peptide information to a
    quantitative ConsensusMap prior to this step
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProteinInference()
        """
        ...
    
    @overload
    def __init__(self, in_0: ProteinInference ) -> None:
        """
        Cython signature: void ProteinInference(ProteinInference &)
        """
        ...
    
    def infer(self, consensus_map: ConsensusMap , reference_map: int ) -> None:
        """
        Cython signature: void infer(ConsensusMap & consensus_map, unsigned int reference_map)
        Given a peptide quantitation, infer corresponding protein quantities
        
        Infers protein ratios from peptide ratios (currently using unique peptides only).
        Use the IDMapper class to add protein and peptide information to a
        quantitative ConsensusMap prior to this step
        
        
        :param consensus_map: Peptide quantitation with ProteinIdentifications attached, where protein quantitation will be attached
        :param reference_map: Index of (iTRAQ) reference channel within the consensus map
        """
        ... 


class Residue:
    """
    Cython implementation of _Residue

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Residue.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Residue()
        """
        ...
    
    @overload
    def __init__(self, in_0: Residue ) -> None:
        """
        Cython signature: void Residue(Residue &)
        """
        ...
    
    @overload
    def __init__(self, name: Union[bytes, str, String] , three_letter_code: Union[bytes, str, String] , one_letter_code: Union[bytes, str, String] , formula: EmpiricalFormula ) -> None:
        """
        Cython signature: void Residue(String name, String three_letter_code, String one_letter_code, EmpiricalFormula formula)
        """
        ...
    
    def getInternalToFull(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getInternalToFull()
        """
        ...
    
    def getInternalToNTerm(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getInternalToNTerm()
        """
        ...
    
    def getInternalToCTerm(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getInternalToCTerm()
        """
        ...
    
    def getInternalToAIon(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getInternalToAIon()
        """
        ...
    
    def getInternalToBIon(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getInternalToBIon()
        """
        ...
    
    def getInternalToCIon(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getInternalToCIon()
        """
        ...
    
    def getInternalToXIon(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getInternalToXIon()
        """
        ...
    
    def getInternalToYIon(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getInternalToYIon()
        """
        ...
    
    def getInternalToZIon(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getInternalToZIon()
        """
        ...
    
    def getResidueTypeName(self, res_type: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String getResidueTypeName(ResidueType res_type)
        Returns the ion name given as a residue type
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the name of the residue
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the residue
        """
        ...
    
    def setSynonyms(self, synonyms: Set[bytes] ) -> None:
        """
        Cython signature: void setSynonyms(libcpp_set[String] synonyms)
        Sets the synonyms
        """
        ...
    
    def addSynonym(self, synonym: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addSynonym(String synonym)
        Adds a synonym
        """
        ...
    
    def getSynonyms(self) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getSynonyms()
        Returns the sysnonyms
        """
        ...
    
    def setThreeLetterCode(self, three_letter_code: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setThreeLetterCode(String three_letter_code)
        Sets the name of the residue as three letter code
        """
        ...
    
    def getThreeLetterCode(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getThreeLetterCode()
        Returns the name of the residue as three letter code
        """
        ...
    
    def setOneLetterCode(self, one_letter_code: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setOneLetterCode(String one_letter_code)
        Sets the name as one letter code
        """
        ...
    
    def getOneLetterCode(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOneLetterCode()
        Returns the name as one letter code
        """
        ...
    
    def addLossFormula(self, in_0: EmpiricalFormula ) -> None:
        """
        Cython signature: void addLossFormula(EmpiricalFormula)
        Adds a neutral loss formula
        """
        ...
    
    def setLossFormulas(self, in_0: List[EmpiricalFormula] ) -> None:
        """
        Cython signature: void setLossFormulas(libcpp_vector[EmpiricalFormula])
        Sets the neutral loss formulas
        """
        ...
    
    def addNTermLossFormula(self, in_0: EmpiricalFormula ) -> None:
        """
        Cython signature: void addNTermLossFormula(EmpiricalFormula)
        Adds N-terminal losses
        """
        ...
    
    def setNTermLossFormulas(self, in_0: List[EmpiricalFormula] ) -> None:
        """
        Cython signature: void setNTermLossFormulas(libcpp_vector[EmpiricalFormula])
        Sets the N-terminal losses
        """
        ...
    
    def getLossFormulas(self) -> List[EmpiricalFormula]:
        """
        Cython signature: libcpp_vector[EmpiricalFormula] getLossFormulas()
        Returns the neutral loss formulas
        """
        ...
    
    def getNTermLossFormulas(self) -> List[EmpiricalFormula]:
        """
        Cython signature: libcpp_vector[EmpiricalFormula] getNTermLossFormulas()
        Returns N-terminal loss formulas
        """
        ...
    
    def setLossNames(self, name: List[bytes] ) -> None:
        """
        Cython signature: void setLossNames(libcpp_vector[String] name)
        Sets the neutral loss molecule name
        """
        ...
    
    def setNTermLossNames(self, name: List[bytes] ) -> None:
        """
        Cython signature: void setNTermLossNames(libcpp_vector[String] name)
        Sets the N-terminal loss names
        """
        ...
    
    def addLossName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addLossName(String name)
        Adds neutral loss molecule name
        """
        ...
    
    def addNTermLossName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addNTermLossName(String name)
        Adds a N-terminal loss name
        """
        ...
    
    def getLossNames(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getLossNames()
        Gets neutral loss name (if there is one, else returns an empty string)
        """
        ...
    
    def getNTermLossNames(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getNTermLossNames()
        Returns the N-terminal loss names
        """
        ...
    
    def setFormula(self, formula: EmpiricalFormula ) -> None:
        """
        Cython signature: void setFormula(EmpiricalFormula formula)
        Sets empirical formula of the residue (must be full, with N and C-terminus)
        """
        ...
    
    @overload
    def getFormula(self, ) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getFormula()
        Returns the empirical formula of the residue
        """
        ...
    
    @overload
    def getFormula(self, res_type: int ) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getFormula(ResidueType res_type)
        """
        ...
    
    def setAverageWeight(self, weight: float ) -> None:
        """
        Cython signature: void setAverageWeight(double weight)
        Sets average weight of the residue (must be full, with N and C-terminus)
        """
        ...
    
    @overload
    def getAverageWeight(self, ) -> float:
        """
        Cython signature: double getAverageWeight()
        Returns average weight of the residue
        """
        ...
    
    @overload
    def getAverageWeight(self, res_type: int ) -> float:
        """
        Cython signature: double getAverageWeight(ResidueType res_type)
        """
        ...
    
    def setMonoWeight(self, weight: float ) -> None:
        """
        Cython signature: void setMonoWeight(double weight)
        Sets monoisotopic weight of the residue (must be full, with N and C-terminus)
        """
        ...
    
    @overload
    def getMonoWeight(self, ) -> float:
        """
        Cython signature: double getMonoWeight()
        Returns monoisotopic weight of the residue
        """
        ...
    
    @overload
    def getMonoWeight(self, res_type: int ) -> float:
        """
        Cython signature: double getMonoWeight(ResidueType res_type)
        """
        ...
    
    def getModification(self) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getModification()
        """
        ...
    
    @overload
    def setModification(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setModification(String name)
        Sets the modification by name; the mod should be present in ModificationsDB
        """
        ...
    
    @overload
    def setModification(self, mod: ResidueModification ) -> None:
        """
        Cython signature: void setModification(const ResidueModification & mod)
        Sets the modification by a ResidueModification object; checks if present in ModificationsDB and adds if not.
        """
        ...
    
    def setModificationByDiffMonoMass(self, diffMonoMass: float ) -> None:
        """
        Cython signature: void setModificationByDiffMonoMass(double diffMonoMass)
        Sets the modification by monoisotopic mass difference in Da; checks if present in ModificationsDB with tolerance and adds a "user-defined" modification if not (for later lookups).
        """
        ...
    
    def getModificationName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getModificationName()
        Returns the name of the modification to the modification
        """
        ...
    
    def setLowMassIons(self, low_mass_ions: List[EmpiricalFormula] ) -> None:
        """
        Cython signature: void setLowMassIons(libcpp_vector[EmpiricalFormula] low_mass_ions)
        Sets the low mass marker ions as a vector of formulas
        """
        ...
    
    def getLowMassIons(self) -> List[EmpiricalFormula]:
        """
        Cython signature: libcpp_vector[EmpiricalFormula] getLowMassIons()
        Returns a vector of formulas with the low mass markers of the residue
        """
        ...
    
    def setResidueSets(self, residues_sets: Set[bytes] ) -> None:
        """
        Cython signature: void setResidueSets(libcpp_set[String] residues_sets)
        Sets the residue sets the amino acid is contained in
        """
        ...
    
    def addResidueSet(self, residue_sets: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addResidueSet(String residue_sets)
        Adds a residue set to the residue sets
        """
        ...
    
    def getResidueSets(self) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getResidueSets()
        Returns the residue sets this residue is contained in
        """
        ...
    
    def hasNeutralLoss(self) -> bool:
        """
        Cython signature: bool hasNeutralLoss()
        True if the residue has neutral loss
        """
        ...
    
    def hasNTermNeutralLosses(self) -> bool:
        """
        Cython signature: bool hasNTermNeutralLosses()
        True if N-terminal neutral losses are set
        """
        ...
    
    def getPka(self) -> float:
        """
        Cython signature: double getPka()
        Returns the pka of the residue
        """
        ...
    
    def getPkb(self) -> float:
        """
        Cython signature: double getPkb()
        Returns the pkb of the residue
        """
        ...
    
    def getPkc(self) -> float:
        """
        Cython signature: double getPkc()
        Returns the pkc of the residue if it exists otherwise -1
        """
        ...
    
    def getPiValue(self) -> float:
        """
        Cython signature: double getPiValue()
        Calculates the isoelectric point using the pk values
        """
        ...
    
    def setPka(self, value: float ) -> None:
        """
        Cython signature: void setPka(double value)
        Sets the pka of the residue
        """
        ...
    
    def setPkb(self, value: float ) -> None:
        """
        Cython signature: void setPkb(double value)
        Sets the pkb of the residue
        """
        ...
    
    def setPkc(self, value: float ) -> None:
        """
        Cython signature: void setPkc(double value)
        Sets the pkc of the residue
        """
        ...
    
    def getSideChainBasicity(self) -> float:
        """
        Cython signature: double getSideChainBasicity()
        Returns the side chain basicity
        """
        ...
    
    def setSideChainBasicity(self, gb_sc: float ) -> None:
        """
        Cython signature: void setSideChainBasicity(double gb_sc)
        Sets the side chain basicity
        """
        ...
    
    def getBackboneBasicityLeft(self) -> float:
        """
        Cython signature: double getBackboneBasicityLeft()
        Returns the backbone basicitiy if located in N-terminal direction
        """
        ...
    
    def setBackboneBasicityLeft(self, gb_bb_l: float ) -> None:
        """
        Cython signature: void setBackboneBasicityLeft(double gb_bb_l)
        Sets the N-terminal direction backbone basicitiy
        """
        ...
    
    def getBackboneBasicityRight(self) -> float:
        """
        Cython signature: double getBackboneBasicityRight()
        Returns the C-terminal direction backbone basicitiy
        """
        ...
    
    def setBackboneBasicityRight(self, gb_bb_r: float ) -> None:
        """
        Cython signature: void setBackboneBasicityRight(double gb_bb_r)
        Sets the C-terminal direction backbone basicity
        """
        ...
    
    def isModified(self) -> bool:
        """
        Cython signature: bool isModified()
        True if the residue is a modified one
        """
        ...
    
    def isInResidueSet(self, residue_set: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool isInResidueSet(String residue_set)
        True if the residue is contained in the set
        """
        ...
    
    def residueTypeToIonLetter(self, res_type: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String residueTypeToIonLetter(ResidueType res_type)
        Helper for mapping residue types to letters for Text annotations and labels
        """
        ...
    
    def __richcmp__(self, other: Residue, op: int) -> Any:
        ...
    ResidueType : __ResidueType 


class ResidueDB:
    """
    Cython implementation of _ResidueDB

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ResidueDB.html>`_
    """
    
    def getNumberOfResidues(self) -> int:
        """
        Cython signature: size_t getNumberOfResidues()
        Returns the number of residues stored
        """
        ...
    
    def getNumberOfModifiedResidues(self) -> int:
        """
        Cython signature: size_t getNumberOfModifiedResidues()
        Returns the number of modified residues stored
        """
        ...
    
    def getResidue(self, name: Union[bytes, str, String] ) -> Residue:
        """
        Cython signature: const Residue * getResidue(const String & name)
        Returns a pointer to the residue with name, 3 letter code or 1 letter code name
        """
        ...
    
    @overload
    def getModifiedResidue(self, name: Union[bytes, str, String] ) -> Residue:
        """
        Cython signature: const Residue * getModifiedResidue(const String & name)
        Returns a pointer to a modified residue given a modification name
        """
        ...
    
    @overload
    def getModifiedResidue(self, residue: Residue , name: Union[bytes, str, String] ) -> Residue:
        """
        Cython signature: const Residue * getModifiedResidue(Residue * residue, const String & name)
        Returns a pointer to a modified residue given a residue and a modification name
        """
        ...
    
    def getResidues(self, residue_set: Union[bytes, str, String] ) -> Set[Residue]:
        """
        Cython signature: libcpp_set[const Residue *] getResidues(const String & residue_set)
        Returns a set of all residues stored in this residue db
        """
        ...
    
    def getResidueSets(self) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getResidueSets()
        Returns all residue sets that are registered which this instance
        """
        ...
    
    def hasResidue(self, name: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasResidue(const String & name)
        Returns true if the db contains a residue with the given name
        """
        ... 


class SimpleSearchEngineAlgorithm:
    """
    Cython implementation of _SimpleSearchEngineAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SimpleSearchEngineAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SimpleSearchEngineAlgorithm()
        """
        ...
    
    @overload
    def __init__(self, in_0: SimpleSearchEngineAlgorithm ) -> None:
        """
        Cython signature: void SimpleSearchEngineAlgorithm(SimpleSearchEngineAlgorithm &)
        """
        ...
    
    def search(self, in_mzML: Union[bytes, str, String] , in_db: Union[bytes, str, String] , prot_ids: List[ProteinIdentification] , pep_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void search(const String & in_mzML, const String & in_db, libcpp_vector[ProteinIdentification] & prot_ids, libcpp_vector[PeptideIdentification] & pep_ids)
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


class SpectrumHelper:
    """
    Cython implementation of _SpectrumHelper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/class_1_1SpectrumHelper.html>`_
    """
    
    removePeaks: __static_SpectrumHelper_removePeaks
    
    removePeaks: __static_SpectrumHelper_removePeaks
    
    subtractMinimumIntensity: __static_SpectrumHelper_subtractMinimumIntensity
    
    subtractMinimumIntensity: __static_SpectrumHelper_subtractMinimumIntensity 


class SplinePackage:
    """
    Cython implementation of _SplinePackage

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SplinePackage.html>`_
    """
    
    @overload
    def __init__(self, pos: List[float] , intensity: List[float] ) -> None:
        """
        Cython signature: void SplinePackage(libcpp_vector[double] pos, libcpp_vector[double] intensity)
        """
        ...
    
    @overload
    def __init__(self, in_0: SplinePackage ) -> None:
        """
        Cython signature: void SplinePackage(SplinePackage &)
        """
        ...
    
    def getPosMin(self) -> float:
        """
        Cython signature: double getPosMin()
        Returns the minimum position for which the spline fit is valid
        """
        ...
    
    def getPosMax(self) -> float:
        """
        Cython signature: double getPosMax()
        Returns the maximum position for which the spline fit is valid
        """
        ...
    
    def getPosStepWidth(self) -> float:
        """
        Cython signature: double getPosStepWidth()
        Returns a sensible position step width for the package
        """
        ...
    
    def isInPackage(self, pos: float ) -> bool:
        """
        Cython signature: bool isInPackage(double pos)
        Returns true if position in
        """
        ...
    
    def eval(self, pos: float ) -> float:
        """
        Cython signature: double eval(double pos)
        Returns interpolated intensity position `pos`
        """
        ... 


class TMTSixPlexQuantitationMethod:
    """
    Cython implementation of _TMTSixPlexQuantitationMethod

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TMTSixPlexQuantitationMethod.html>`_
      -- Inherits from ['IsobaricQuantitationMethod']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TMTSixPlexQuantitationMethod()
        """
        ...
    
    @overload
    def __init__(self, in_0: TMTSixPlexQuantitationMethod ) -> None:
        """
        Cython signature: void TMTSixPlexQuantitationMethod(TMTSixPlexQuantitationMethod &)
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


class Tagger:
    """
    Cython implementation of _Tagger

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Tagger.html>`_

    Constructor for Tagger
    
    The parameter `max_charge_` should be >= `min_charge_`
    Also `max_tag_length` should be >= `min_tag_length`
    
    :param min_tag_length: The minimal sequence tag length
    :param ppm: The tolerance for matching residue masses to peak delta masses
    :param max_tag_length: The maximal sequence tag length
    :param min_charge: Minimal fragment charge considered for each sequence tag
    :param max_charge: Maximal fragment charge considered for each sequence tag
    :param fixed_mods: A list of modification names. The modified residues replace the unmodified versions
    :param var_mods: A list of modification names. The modified residues are added as additional entries to the list of residues
    """
    
    @overload
    def __init__(self, in_0: Tagger ) -> None:
        """
        Cython signature: void Tagger(Tagger &)
        """
        ...
    
    @overload
    def __init__(self, min_tag_length: int , ppm: float , max_tag_length: int , min_charge: int , max_charge: int , fixed_mods: List[bytes] , var_mods: List[bytes] ) -> None:
        """
        Cython signature: void Tagger(size_t min_tag_length, double ppm, size_t max_tag_length, size_t min_charge, size_t max_charge, const StringList & fixed_mods, const StringList & var_mods)
        """
        ...
    
    @overload
    def getTag(self, mzs: List[float] , tags: List[Union[bytes, str]] ) -> None:
        """
        Cython signature: void getTag(const libcpp_vector[double] & mzs, libcpp_vector[libcpp_utf8_string] & tags)
        Generate tags from mass vector `mzs`
        
        The parameter `tags` is filled with one string per sequence tag
        It uses the standard residues from ResidueDB including
        the fixed and variable modifications given to the constructor
        
        :param mzs: A vector of mz values, containing the mz values from a centroided fragment spectrum
        :param tags: The vector of tags, that is filled with this function
        """
        ...
    
    @overload
    def getTag(self, spec: MSSpectrum , tags: List[Union[bytes, str]] ) -> None:
        """
        Cython signature: void getTag(const MSSpectrum & spec, libcpp_vector[libcpp_utf8_string] & tags)
        Generate tags from an MSSpectrum
        
        The parameter `tags` is filled with one string per sequence tag
        It uses the standard residues from ResidueDB including
        the fixed and variable modifications given to the constructor
        
        :param spec: A centroided fragment spectrum
        :param tags: The vector of tags, that is filled with this function
        """
        ...
    
    def setMaxCharge(self, max_charge: int ) -> None:
        """
        Cython signature: void setMaxCharge(size_t max_charge)
        Change the maximal charge considered by the tagger
        
        Allows to change the maximal considered charge e.g. based on a spectra
        precursor charge without calling the constructor multiple times
        
        :param max_charge: The new maximal charge
        """
        ... 


class Tagging:
    """
    Cython implementation of _Tagging

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Tagging.html>`_

    Meta information about tagging of a sample e.g. ICAT labeling
    
    Holds information about the mass difference between light and heavy tag
    All other relevant information is provided by Modification
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Tagging()
        """
        ...
    
    @overload
    def __init__(self, in_0: Tagging ) -> None:
        """
        Cython signature: void Tagging(Tagging &)
        """
        ...
    
    def getMassShift(self) -> float:
        """
        Cython signature: double getMassShift()
        Returns the mass difference between light and heavy variant (default is 0.0)
        """
        ...
    
    def setMassShift(self, mass_shift: float ) -> None:
        """
        Cython signature: void setMassShift(double mass_shift)
        Sets the mass difference between light and heavy variant
        """
        ...
    
    def getVariant(self) -> int:
        """
        Cython signature: IsotopeVariant getVariant()
        Returns the isotope variant of the tag (default is LIGHT)
        """
        ...
    
    def setVariant(self, variant: int ) -> None:
        """
        Cython signature: void setVariant(IsotopeVariant variant)
        Sets the isotope variant of the tag
        """
        ... 


class TextFile:
    """
    Cython implementation of _TextFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TextFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TextFile()
        This class provides some basic file handling methods for text files
        """
        ...
    
    @overload
    def __init__(self, in_0: TextFile ) -> None:
        """
        Cython signature: void TextFile(TextFile &)
        """
        ...
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] , trim_linesalse: bool , first_n1: int ) -> None:
        """
        Cython signature: void TextFile(const String & filename, bool trim_linesalse, int first_n1)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , trim_linesalse: bool , first_n1: int ) -> None:
        """
        Cython signature: void load(const String & filename, bool trim_linesalse, int first_n1)
        Loads data from a text file
        
        :param filename: The input file name
        :param trim_lines: Whether or not the lines are trimmed when reading them from file
        :param first_n: If set, only `first_n` lines the lines from the beginning of the file are read
        :param skip_empty_lines: Should empty lines be skipped? If used in conjunction with `trim_lines`, also lines with only whitespace will be skipped. Skipped lines do not count towards the total number of read lines
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void store(const String & filename)
        Writes the data to a file
        """
        ...
    
    def addLine(self, line: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addLine(const String line)
        """
        ... 


class XQuestScores:
    """
    Cython implementation of _XQuestScores

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1XQuestScores.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void XQuestScores()
        """
        ...
    
    @overload
    def __init__(self, in_0: XQuestScores ) -> None:
        """
        Cython signature: void XQuestScores(XQuestScores &)
        """
        ...
    
    @overload
    def preScore(self, matched_alpha: int , ions_alpha: int , matched_beta: int , ions_beta: int ) -> float:
        """
        Cython signature: float preScore(size_t matched_alpha, size_t ions_alpha, size_t matched_beta, size_t ions_beta)
        Compute a simple and fast to compute pre-score for a cross-link spectrum match
        
        :param matched_alpha: Number of experimental peaks matched to theoretical linear ions from the alpha peptide
        :param ions_alpha: Number of theoretical ions from the alpha peptide
        :param matched_beta: Number of experimental peaks matched to theoretical linear ions from the beta peptide
        :param ions_beta: Number of theoretical ions from the beta peptide
        """
        ...
    
    @overload
    def preScore(self, matched_alpha: int , ions_alpha: int ) -> float:
        """
        Cython signature: float preScore(size_t matched_alpha, size_t ions_alpha)
        Compute a simple and fast to compute pre-score for a mono-link spectrum match
        
        :param matched_alpha: Number of experimental peaks matched to theoretical linear ions from the alpha peptide
        :param ions_alpha: Number of theoretical ions from the alpha peptide
        """
        ...
    
    def matchOddsScore(self, theoretical_spec: MSSpectrum , fragment_mass_tolerance: float , fragment_mass_tolerance_unit_ppm: bool , is_xlink_spectrum: bool , n_charges: int ) -> float:
        """
        Cython signature: double matchOddsScore(MSSpectrum & theoretical_spec, double fragment_mass_tolerance, bool fragment_mass_tolerance_unit_ppm, bool is_xlink_spectrum, size_t n_charges)
        Compute the match-odds score, a score based on the probability of getting the given number of matched peaks by chance
        
        :param theoretical_spec: Theoretical spectrum, sorted by position
        :param matched_size: Alignment between the theoretical and the experimental spectra
        :param fragment_mass_tolerance: Fragment mass tolerance of the alignment
        :param fragment_mass_tolerance_unit_ppm: Fragment mass tolerance unit of the alignment, true = ppm, false = Da
        :param is_xlink_spectrum: Type of cross-link, true = cross-link, false = mono-link
        :param n_charges: Number of considered charges in the theoretical spectrum
        """
        ...
    
    def logOccupancyProb(self, theoretical_spec: MSSpectrum , matched_size: int , fragment_mass_tolerance: float , fragment_mass_tolerance_unit_ppm: bool ) -> float:
        """
        Cython signature: double logOccupancyProb(MSSpectrum theoretical_spec, size_t matched_size, double fragment_mass_tolerance, bool fragment_mass_tolerance_unit_ppm)
        Compute the logOccupancyProb score, similar to the match_odds, a score based on the probability of getting the given number of matched peaks by chance
        
        :param theoretical_spec: Theoretical spectrum, sorted by position
        :param matched_size: Number of matched peaks between experimental and theoretical spectra
        :param fragment_mass_tolerance: The tolerance of the alignment
        :param fragment_mass_tolerance_unit: The tolerance unit of the alignment, true = ppm, false = Da
        """
        ...
    
    def weightedTICScoreXQuest(self, alpha_size: int , beta_size: int , intsum_alpha: float , intsum_beta: float , total_current: float , type_is_cross_link: bool ) -> float:
        """
        Cython signature: double weightedTICScoreXQuest(size_t alpha_size, size_t beta_size, double intsum_alpha, double intsum_beta, double total_current, bool type_is_cross_link)
        """
        ...
    
    def weightedTICScore(self, alpha_size: int , beta_size: int , intsum_alpha: float , intsum_beta: float , total_current: float , type_is_cross_link: bool ) -> float:
        """
        Cython signature: double weightedTICScore(size_t alpha_size, size_t beta_size, double intsum_alpha, double intsum_beta, double total_current, bool type_is_cross_link)
        """
        ...
    
    def matchedCurrentChain(self, matched_spec_common: List[List[int, int]] , matched_spec_xlinks: List[List[int, int]] , spectrum_common_peaks: MSSpectrum , spectrum_xlink_peaks: MSSpectrum ) -> float:
        """
        Cython signature: double matchedCurrentChain(libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_common, libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_xlinks, MSSpectrum & spectrum_common_peaks, MSSpectrum & spectrum_xlink_peaks)
        """
        ...
    
    def totalMatchedCurrent(self, matched_spec_common_alpha: List[List[int, int]] , matched_spec_common_beta: List[List[int, int]] , matched_spec_xlinks_alpha: List[List[int, int]] , matched_spec_xlinks_beta: List[List[int, int]] , spectrum_common_peaks: MSSpectrum , spectrum_xlink_peaks: MSSpectrum ) -> float:
        """
        Cython signature: double totalMatchedCurrent(libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_common_alpha, libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_common_beta, libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_xlinks_alpha, libcpp_vector[libcpp_pair[size_t,size_t]] & matched_spec_xlinks_beta, MSSpectrum & spectrum_common_peaks, MSSpectrum & spectrum_xlink_peaks)
        """
        ...
    
    def xCorrelation(self, spec1: MSSpectrum , spec2: MSSpectrum , maxshift: int , tolerance: float ) -> List[float]:
        """
        Cython signature: libcpp_vector[double] xCorrelation(MSSpectrum & spec1, MSSpectrum & spec2, int maxshift, double tolerance)
        """
        ...
    
    def xCorrelationPrescore(self, spec1: MSSpectrum , spec2: MSSpectrum , tolerance: float ) -> float:
        """
        Cython signature: double xCorrelationPrescore(MSSpectrum & spec1, MSSpectrum & spec2, double tolerance)
        """
        ... 


class _Interfaces_BinaryDataArray:
    """
    Cython implementation of _BinaryDataArray

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Interfaces_1_1BinaryDataArray.html>`_
    """
    
    data: List[float]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void _Interfaces_BinaryDataArray()
        """
        ...
    
    @overload
    def __init__(self, in_0: _Interfaces_BinaryDataArray ) -> None:
        """
        Cython signature: void _Interfaces_BinaryDataArray(_Interfaces_BinaryDataArray &)
        """
        ... 


class _Interfaces_Chromatogram:
    """
    Cython implementation of _Chromatogram

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Interfaces_1_1Chromatogram.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void _Interfaces_Chromatogram()
        """
        ...
    
    @overload
    def __init__(self, in_0: _Interfaces_Chromatogram ) -> None:
        """
        Cython signature: void _Interfaces_Chromatogram(_Interfaces_Chromatogram &)
        """
        ... 


class _Interfaces_Spectrum:
    """
    Cython implementation of _Spectrum

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Interfaces_1_1Spectrum.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void _Interfaces_Spectrum()
        """
        ...
    
    @overload
    def __init__(self, in_0: _Interfaces_Spectrum ) -> None:
        """
        Cython signature: void _Interfaces_Spectrum(_Interfaces_Spectrum &)
        """
        ... 


class BoundaryCondition:
    None
    BC_ZERO_ENDPOINTS : int
    BC_ZERO_FIRST : int
    BC_ZERO_SECOND : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class FileType:
    None
    UNKNOWN : int
    DTA : int
    DTA2D : int
    MZDATA : int
    MZXML : int
    FEATUREXML : int
    IDXML : int
    CONSENSUSXML : int
    MGF : int
    INI : int
    TOPPAS : int
    TRANSFORMATIONXML : int
    MZML : int
    CACHEDMZML : int
    MS2 : int
    PEPXML : int
    PROTXML : int
    MZIDENTML : int
    QCML : int
    GELML : int
    TRAML : int
    MSP : int
    OMSSAXML : int
    MASCOTXML : int
    PNG : int
    XMASS : int
    TSV : int
    PEPLIST : int
    HARDKLOER : int
    KROENIK : int
    FASTA : int
    EDTA : int
    CSV : int
    TXT : int
    OBO : int
    HTML : int
    XML : int
    ANALYSISXML : int
    XSD : int
    PSQ : int
    MRM : int
    SQMASS : int
    PQP : int
    OSW : int
    PSMS : int
    PARAMXML : int
    SIZE_OF_TYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __InletType:
    None
    INLETNULL : int
    DIRECT : int
    BATCH : int
    CHROMATOGRAPHY : int
    PARTICLEBEAM : int
    MEMBRANESEPARATOR : int
    OPENSPLIT : int
    JETSEPARATOR : int
    SEPTUM : int
    RESERVOIR : int
    MOVINGBELT : int
    MOVINGWIRE : int
    FLOWINJECTIONANALYSIS : int
    ELECTROSPRAYINLET : int
    THERMOSPRAYINLET : int
    INFUSION : int
    CONTINUOUSFLOWFASTATOMBOMBARDMENT : int
    INDUCTIVELYCOUPLEDPLASMA : int
    MEMBRANE : int
    NANOSPRAY : int
    SIZE_OF_INLETTYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __IonizationMethod:
    None
    IONMETHODNULL : int
    ESI : int
    EI : int
    CI : int
    FAB : int
    TSP : int
    LD : int
    FD : int
    FI : int
    PD : int
    SI : int
    TI : int
    API : int
    ISI : int
    CID : int
    CAD : int
    HN : int
    APCI : int
    APPI : int
    ICP : int
    NESI : int
    MESI : int
    SELDI : int
    SEND : int
    FIB : int
    MALDI : int
    MPI : int
    DI : int
    FA : int
    FII : int
    GD_MS : int
    NICI : int
    NRMS : int
    PI : int
    PYMS : int
    REMPI : int
    AI : int
    ASI : int
    AD : int
    AUI : int
    CEI : int
    CHEMI : int
    DISSI : int
    LSI : int
    PEI : int
    SOI : int
    SPI : int
    SUI : int
    VI : int
    AP_MALDI : int
    SILI : int
    SALDI : int
    SIZE_OF_IONIZATIONMETHOD : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class IsotopeVariant:
    None
    LIGHT : int
    HEAVY : int
    SIZE_OF_ISOTOPEVARIANT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __Polarity:
    None
    POLNULL : int
    POSITIVE : int
    NEGATIVE : int
    SIZE_OF_POLARITY : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __ResidueType:
    None
    Full : int
    Internal : int
    NTerminal : int
    CTerminal : int
    AIon : int
    BIon : int
    CIon : int
    XIon : int
    YIon : int
    ZIon : int
    Precursor_ion : int
    BIonMinusH20 : int
    YIonMinusH20 : int
    BIonMinusNH3 : int
    YIonMinusNH3 : int
    NonIdentified : int
    Unannotated : int
    SizeOfResidueType : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __Specificity:
    None
    SPEC_NONE : int
    SPEC_SEMI : int
    SPEC_FULL : int
    SPEC_UNKNOWN : int
    SPEC_NOCTERM : int
    SPEC_NONTERM : int
    SIZE_OF_SPECIFICITY : int

    def getMapping(self) -> Dict[int, str]:
       ... 

