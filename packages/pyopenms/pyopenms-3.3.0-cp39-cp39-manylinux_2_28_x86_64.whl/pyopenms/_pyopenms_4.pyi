from __future__ import annotations
from typing import overload, Any, List, Dict, Tuple, Set, Sequence, Union
from pyopenms import *  # pylint: disable=wildcard-import; lgtm(py/polluting-import)
import numpy as _np

from enum import Enum as _PyEnum


def __static_MZTrafoModel_enumToName(mt: int ) -> bytes:
    """
    Cython signature: libcpp_string enumToName(MZTrafoModel_MODELTYPE mt)
    """
    ...

def __static_MZTrafoModel_findNearest(tms: List[MZTrafoModel] , rt: float ) -> int:
    """
    Cython signature: size_t findNearest(libcpp_vector[MZTrafoModel] & tms, double rt)
    """
    ...

def __static_MZTrafoModel_isValidModel(trafo: MZTrafoModel ) -> bool:
    """
    Cython signature: bool isValidModel(MZTrafoModel & trafo)
    """
    ...

def __static_ExperimentalDesignFile_load(tsv_file: Union[bytes, str, String] , in_1: bool ) -> ExperimentalDesign:
    """
    Cython signature: ExperimentalDesign load(const String & tsv_file, bool)
    """
    ...

def __static_MZTrafoModel_nameToEnum(name: bytes ) -> int:
    """
    Cython signature: MZTrafoModel_MODELTYPE nameToEnum(libcpp_string name)
    """
    ...

def __static_MZTrafoModel_setCoefficientLimits(offset: float , scale: float , power: float ) -> None:
    """
    Cython signature: void setCoefficientLimits(double offset, double scale, double power)
    """
    ...

def __static_MZTrafoModel_setRANSACParams(p: RANSACParam ) -> None:
    """
    Cython signature: void setRANSACParams(RANSACParam p)
    """
    ...

def __static_PercolatorInfile_store(pin_file: Union[bytes, str, String] , peptide_ids: List[PeptideIdentification] , feature_set: List[bytes] , in_3: bytes , min_charge: int , max_charge: int ) -> None:
    """
    Cython signature: void store(String pin_file, libcpp_vector[PeptideIdentification] peptide_ids, StringList feature_set, libcpp_string, int min_charge, int max_charge)
    """
    ...


class AbsoluteQuantitationMethodFile:
    """
    Cython implementation of _AbsoluteQuantitationMethodFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AbsoluteQuantitationMethodFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AbsoluteQuantitationMethodFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: AbsoluteQuantitationMethodFile ) -> None:
        """
        Cython signature: void AbsoluteQuantitationMethodFile(AbsoluteQuantitationMethodFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , aqm_list: List[AbsoluteQuantitationMethod] ) -> None:
        """
        Cython signature: void load(const String & filename, libcpp_vector[AbsoluteQuantitationMethod] & aqm_list)
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , aqm_list: List[AbsoluteQuantitationMethod] ) -> None:
        """
        Cython signature: void store(const String & filename, libcpp_vector[AbsoluteQuantitationMethod] & aqm_list)
        """
        ... 


class AccurateMassSearchResult:
    """
    Cython implementation of _AccurateMassSearchResult

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AccurateMassSearchResult.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void AccurateMassSearchResult()
        """
        ...
    
    def getObservedMZ(self) -> float:
        """
        Cython signature: double getObservedMZ()
        """
        ...
    
    def setObservedMZ(self, m: float ) -> None:
        """
        Cython signature: void setObservedMZ(double & m)
        """
        ...
    
    def getCalculatedMZ(self) -> float:
        """
        Cython signature: double getCalculatedMZ()
        """
        ...
    
    def setCalculatedMZ(self, m: float ) -> None:
        """
        Cython signature: void setCalculatedMZ(double & m)
        """
        ...
    
    def getQueryMass(self) -> float:
        """
        Cython signature: double getQueryMass()
        """
        ...
    
    def setQueryMass(self, m: float ) -> None:
        """
        Cython signature: void setQueryMass(double & m)
        """
        ...
    
    def getFoundMass(self) -> float:
        """
        Cython signature: double getFoundMass()
        """
        ...
    
    def setFoundMass(self, m: float ) -> None:
        """
        Cython signature: void setFoundMass(double & m)
        """
        ...
    
    def getCharge(self) -> float:
        """
        Cython signature: double getCharge()
        """
        ...
    
    def setCharge(self, ch: float ) -> None:
        """
        Cython signature: void setCharge(double & ch)
        """
        ...
    
    def getMZErrorPPM(self) -> float:
        """
        Cython signature: double getMZErrorPPM()
        """
        ...
    
    def setMZErrorPPM(self, ppm: float ) -> None:
        """
        Cython signature: void setMZErrorPPM(double & ppm)
        """
        ...
    
    def getObservedRT(self) -> float:
        """
        Cython signature: double getObservedRT()
        """
        ...
    
    def setObservedRT(self, rt: float ) -> None:
        """
        Cython signature: void setObservedRT(double & rt)
        """
        ...
    
    def getObservedIntensity(self) -> float:
        """
        Cython signature: double getObservedIntensity()
        """
        ...
    
    def setObservedIntensity(self, intensity: float ) -> None:
        """
        Cython signature: void setObservedIntensity(double & intensity)
        """
        ...
    
    def getMatchingIndex(self) -> float:
        """
        Cython signature: double getMatchingIndex()
        """
        ...
    
    def setMatchingIndex(self, idx: float ) -> None:
        """
        Cython signature: void setMatchingIndex(double & idx)
        """
        ...
    
    def getFoundAdduct(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFoundAdduct()
        """
        ...
    
    def setFoundAdduct(self, add: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFoundAdduct(const String & add)
        """
        ...
    
    def getFormulaString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFormulaString()
        """
        ...
    
    def setEmpiricalFormula(self, ep: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setEmpiricalFormula(const String & ep)
        """
        ...
    
    def getMatchingHMDBids(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getMatchingHMDBids()
        """
        ...
    
    def setMatchingHMDBids(self, match_ids: List[bytes] ) -> None:
        """
        Cython signature: void setMatchingHMDBids(libcpp_vector[String] & match_ids)
        """
        ...
    
    def getIsotopesSimScore(self) -> float:
        """
        Cython signature: double getIsotopesSimScore()
        """
        ...
    
    def setIsotopesSimScore(self, sim_score: float ) -> None:
        """
        Cython signature: void setIsotopesSimScore(double & sim_score)
        """
        ...
    
    def getIndividualIntensities(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] getIndividualIntensities()
        """
        ...
    
    def setIndividualIntensities(self, in_0: List[float] ) -> None:
        """
        Cython signature: void setIndividualIntensities(libcpp_vector[double])
        """
        ...
    
    def getSourceFeatureIndex(self) -> int:
        """
        Cython signature: size_t getSourceFeatureIndex()
        """
        ...
    
    def setSourceFeatureIndex(self, in_0: int ) -> None:
        """
        Cython signature: void setSourceFeatureIndex(size_t)
        """
        ...
    
    def getMasstraceIntensities(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] getMasstraceIntensities()
        """
        ...
    
    def setMasstraceIntensities(self, in_0: List[float] ) -> None:
        """
        Cython signature: void setMasstraceIntensities(libcpp_vector[double] &)
        """
        ... 


class AcquisitionInfo:
    """
    Cython implementation of _AcquisitionInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AcquisitionInfo.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AcquisitionInfo()
        """
        ...
    
    @overload
    def __init__(self, in_0: AcquisitionInfo ) -> None:
        """
        Cython signature: void AcquisitionInfo(AcquisitionInfo &)
        """
        ...
    
    def getMethodOfCombination(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getMethodOfCombination()
        Returns the method of combination
        """
        ...
    
    def setMethodOfCombination(self, method: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setMethodOfCombination(String method)
        Sets the method of combination
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        Number a Acquisition objects
        """
        ...
    
    def __getitem__(self, in_0: int ) -> Acquisition:
        """
        Cython signature: Acquisition & operator[](size_t)
        """
        ...
    def __setitem__(self, key: int, value: Acquisition ) -> None:
        """Cython signature: Acquisition & operator[](size_t)"""
        ...
    
    def push_back(self, in_0: Acquisition ) -> None:
        """
        Cython signature: void push_back(Acquisition)
        Append a Acquisition object
        """
        ...
    
    def resize(self, n: int ) -> None:
        """
        Cython signature: void resize(size_t n)
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
    
    def __richcmp__(self, other: AcquisitionInfo, op: int) -> Any:
        ... 


class BinnedSpectrum:
    """
    Cython implementation of _BinnedSpectrum

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1BinnedSpectrum.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void BinnedSpectrum()
        """
        ...
    
    @overload
    def __init__(self, in_0: BinnedSpectrum ) -> None:
        """
        Cython signature: void BinnedSpectrum(BinnedSpectrum &)
        """
        ...
    
    @overload
    def __init__(self, in_0: MSSpectrum , size: float , unit_ppm: bool , spread: int , offset: float ) -> None:
        """
        Cython signature: void BinnedSpectrum(MSSpectrum, float size, bool unit_ppm, unsigned int spread, float offset)
        """
        ...
    
    def getBinSize(self) -> float:
        """
        Cython signature: float getBinSize()
        Returns the bin size
        """
        ...
    
    def getBinSpread(self) -> int:
        """
        Cython signature: unsigned int getBinSpread()
        Returns the bin spread
        """
        ...
    
    def getBinIndex(self, mz: float ) -> int:
        """
        Cython signature: unsigned int getBinIndex(float mz)
        Returns the bin index of a given m/z position
        """
        ...
    
    def getBinLowerMZ(self, i: int ) -> float:
        """
        Cython signature: float getBinLowerMZ(size_t i)
        Returns the lower m/z of a bin given its index
        """
        ...
    
    def getBinIntensity(self, mz: float ) -> float:
        """
        Cython signature: float getBinIntensity(double mz)
        Returns the bin intensity at a given m/z position
        """
        ...
    
    def getPrecursors(self) -> List[Precursor]:
        """
        Cython signature: libcpp_vector[Precursor] getPrecursors()
        """
        ...
    
    def isCompatible(self, a: BinnedSpectrum , b: BinnedSpectrum ) -> bool:
        """
        Cython signature: bool isCompatible(BinnedSpectrum & a, BinnedSpectrum & b)
        """
        ...
    
    def getOffset(self) -> float:
        """
        Cython signature: float getOffset()
        Returns offset
        """
        ...
    
    def __richcmp__(self, other: BinnedSpectrum, op: int) -> Any:
        ... 


class ChargedIndexSet:
    """
    Cython implementation of _ChargedIndexSet

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ChargedIndexSet.html>`_
    """
    
    charge: int
    
    def __init__(self) -> None:
        """
        Cython signature: void ChargedIndexSet()
        Index set with associated charge estimate
        """
        ... 


class ConsensusIDAlgorithm:
    """
    Cython implementation of _ConsensusIDAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusIDAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler']
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


class ConsensusIDAlgorithmBest:
    """
    Cython implementation of _ConsensusIDAlgorithmBest

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusIDAlgorithmBest.html>`_
      -- Inherits from ['ConsensusIDAlgorithmIdentity']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusIDAlgorithmBest()
        """
        ...
    
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


class ConsensusIDAlgorithmIdentity:
    """
    Cython implementation of _ConsensusIDAlgorithmIdentity

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusIDAlgorithmIdentity.html>`_
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


class ConsensusIDAlgorithmWorst:
    """
    Cython implementation of _ConsensusIDAlgorithmWorst

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusIDAlgorithmWorst.html>`_
      -- Inherits from ['ConsensusIDAlgorithmIdentity']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusIDAlgorithmWorst()
        """
        ...
    
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


class ContactPerson:
    """
    Cython implementation of _ContactPerson

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ContactPerson.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ContactPerson()
        """
        ...
    
    @overload
    def __init__(self, in_0: ContactPerson ) -> None:
        """
        Cython signature: void ContactPerson(ContactPerson &)
        """
        ...
    
    def getFirstName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFirstName()
        Returns the first name of the person
        """
        ...
    
    def setFirstName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFirstName(String name)
        Sets the first name of the person
        """
        ...
    
    def getLastName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getLastName()
        Returns the last name of the person
        """
        ...
    
    def setLastName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setLastName(String name)
        Sets the last name of the person
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the full name of the person (gets split into first and last name internally)
        """
        ...
    
    def getInstitution(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getInstitution()
        Returns the affiliation
        """
        ...
    
    def setInstitution(self, institution: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setInstitution(String institution)
        Sets the affiliation
        """
        ...
    
    def getEmail(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getEmail()
        Returns the email address
        """
        ...
    
    def setEmail(self, email: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setEmail(String email)
        Sets the email address
        """
        ...
    
    def getURL(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getURL()
        Returns the URL associated with the contact person (e.g., the institute webpage
        """
        ...
    
    def setURL(self, email: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setURL(String email)
        Sets the URL associated with the contact person (e.g., the institute webpage
        """
        ...
    
    def getAddress(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getAddress()
        Returns the address
        """
        ...
    
    def setAddress(self, email: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setAddress(String email)
        Sets the address
        """
        ...
    
    def getContactInfo(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getContactInfo()
        Returns miscellaneous info about the contact person
        """
        ...
    
    def setContactInfo(self, contact_info: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setContactInfo(String contact_info)
        Sets miscellaneous info about the contact person
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
    
    def __richcmp__(self, other: ContactPerson, op: int) -> Any:
        ... 


class DataFilter:
    """
    Cython implementation of _DataFilter

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DataFilter.html>`_
    """
    
    field: int
    
    op: int
    
    value: float
    
    value_string: Union[bytes, str, String]
    
    meta_name: Union[bytes, str, String]
    
    value_is_numerical: bool
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DataFilter()
        """
        ...
    
    @overload
    def __init__(self, in_0: DataFilter ) -> None:
        """
        Cython signature: void DataFilter(DataFilter &)
        """
        ...
    
    def toString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        """
        ...
    
    def fromString(self, filter_: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void fromString(const String & filter_)
        """
        ...
    
    def __str__(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        """
        ...
    
    def __richcmp__(self, other: DataFilter, op: int) -> Any:
        ... 


class DataFilters:
    """
    Cython implementation of _DataFilters

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DataFilters.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DataFilters()
        """
        ...
    
    @overload
    def __init__(self, in_0: DataFilters ) -> None:
        """
        Cython signature: void DataFilters(DataFilters &)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ...
    
    def __getitem__(self, in_0: int ) -> DataFilter:
        """
        Cython signature: DataFilter operator[](size_t)
        """
        ...
    
    def add(self, filter_: DataFilter ) -> None:
        """
        Cython signature: void add(DataFilter & filter_)
        """
        ...
    
    def remove(self, index: int ) -> None:
        """
        Cython signature: void remove(size_t index)
        """
        ...
    
    def replace(self, index: int , filter_: DataFilter ) -> None:
        """
        Cython signature: void replace(size_t index, DataFilter & filter_)
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ...
    
    def setActive(self, is_active: bool ) -> None:
        """
        Cython signature: void setActive(bool is_active)
        """
        ...
    
    def isActive(self) -> bool:
        """
        Cython signature: bool isActive()
        """
        ...
    
    @overload
    def passes(self, feature: Feature ) -> bool:
        """
        Cython signature: bool passes(Feature & feature)
        """
        ...
    
    @overload
    def passes(self, consensus_feature: ConsensusFeature ) -> bool:
        """
        Cython signature: bool passes(ConsensusFeature & consensus_feature)
        """
        ...
    
    @overload
    def passes(self, spectrum: MSSpectrum , peak_index: int ) -> bool:
        """
        Cython signature: bool passes(MSSpectrum & spectrum, size_t peak_index)
        """
        ...
    FilterOperation : __FilterOperation
    FilterType : __FilterType 


class DataProcessing:
    """
    Cython implementation of _DataProcessing

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DataProcessing.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DataProcessing()
        """
        ...
    
    @overload
    def __init__(self, in_0: DataProcessing ) -> None:
        """
        Cython signature: void DataProcessing(DataProcessing &)
        """
        ...
    
    def setProcessingActions(self, in_0: Set[int] ) -> None:
        """
        Cython signature: void setProcessingActions(libcpp_set[ProcessingAction])
        """
        ...
    
    def getProcessingActions(self) -> Set[int]:
        """
        Cython signature: libcpp_set[ProcessingAction] getProcessingActions()
        """
        ...
    
    def getSoftware(self) -> Software:
        """
        Cython signature: Software getSoftware()
        """
        ...
    
    def setSoftware(self, s: Software ) -> None:
        """
        Cython signature: void setSoftware(Software s)
        """
        ...
    
    def getCompletionTime(self) -> DateTime:
        """
        Cython signature: DateTime getCompletionTime()
        """
        ...
    
    def setCompletionTime(self, t: DateTime ) -> None:
        """
        Cython signature: void setCompletionTime(DateTime t)
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
    
    def __richcmp__(self, other: DataProcessing, op: int) -> Any:
        ...
    ProcessingAction : __ProcessingAction 


class DataValue:
    """
    Cython implementation of _DataValue

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DataValue.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DataValue()
        """
        ...
    
    @overload
    def __init__(self, in_0: DataValue ) -> None:
        """
        Cython signature: void DataValue(DataValue &)
        """
        ...
    
    @overload
    def __init__(self, in_0: bytes ) -> None:
        """
        Cython signature: void DataValue(char *)
        """
        ...
    
    @overload
    def __init__(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void DataValue(const String &)
        """
        ...
    
    @overload
    def __init__(self, in_0: int ) -> None:
        """
        Cython signature: void DataValue(int)
        """
        ...
    
    @overload
    def __init__(self, in_0: float ) -> None:
        """
        Cython signature: void DataValue(double)
        """
        ...
    
    @overload
    def __init__(self, in_0: List[bytes] ) -> None:
        """
        Cython signature: void DataValue(StringList)
        """
        ...
    
    @overload
    def __init__(self, in_0: List[int] ) -> None:
        """
        Cython signature: void DataValue(IntList)
        """
        ...
    
    @overload
    def __init__(self, in_0: List[float] ) -> None:
        """
        Cython signature: void DataValue(DoubleList)
        """
        ...
    
    @overload
    def __init__(self, in_0: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void DataValue(ParamValue)
        """
        ...
    
    def toStringList(self) -> List[bytes]:
        """
        Cython signature: StringList toStringList()
        """
        ...
    
    def toDoubleList(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] toDoubleList()
        """
        ...
    
    def toIntList(self) -> List[int]:
        """
        Cython signature: libcpp_vector[int] toIntList()
        """
        ...
    
    def toString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        """
        ...
    
    def toBool(self) -> bool:
        """
        Cython signature: bool toBool()
        """
        ...
    
    def valueType(self) -> int:
        """
        Cython signature: DataType valueType()
        """
        ...
    
    def isEmpty(self) -> int:
        """
        Cython signature: int isEmpty()
        """
        ...
    
    def getUnitType(self) -> int:
        """
        Cython signature: UnitType getUnitType()
        """
        ...
    
    def setUnitType(self, u: int ) -> None:
        """
        Cython signature: void setUnitType(UnitType u)
        """
        ...
    
    def hasUnit(self) -> bool:
        """
        Cython signature: bool hasUnit()
        """
        ...
    
    def getUnit(self) -> int:
        """
        Cython signature: int getUnit()
        """
        ...
    
    def setUnit(self, unit_id: int ) -> None:
        """
        Cython signature: void setUnit(int unit_id)
        """
        ...
    
    def __str__(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        """
        ... 


class DecoyGenerator:
    """
    Cython implementation of _DecoyGenerator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DecoyGenerator.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DecoyGenerator()
        """
        ...
    
    @overload
    def __init__(self, in_0: DecoyGenerator ) -> None:
        """
        Cython signature: void DecoyGenerator(DecoyGenerator &)
        """
        ...
    
    def setSeed(self, in_0: int ) -> None:
        """
        Cython signature: void setSeed(uint64_t)
        """
        ...
    
    def reverseProtein(self, protein: AASequence ) -> AASequence:
        """
        Cython signature: AASequence reverseProtein(const AASequence & protein)
        Reverses the protein sequence
        """
        ...
    
    def reversePeptides(self, protein: AASequence , protease: Union[bytes, str, String] ) -> AASequence:
        """
        Cython signature: AASequence reversePeptides(const AASequence & protein, const String & protease)
        Reverses the protein's peptide sequences between enzymatic cutting positions
        """
        ...
    
    def shufflePeptides(self, aas: AASequence , protease: Union[bytes, str, String] , max_attempts: int ) -> AASequence:
        """
        Cython signature: AASequence shufflePeptides(const AASequence & aas, const String & protease, const int max_attempts)
        Shuffle the protein's peptide sequences between enzymatic cutting positions, each peptide is shuffled @param max_attempts times to minimize sequence identity
        """
        ... 


class ElutionPeakDetection:
    """
    Cython implementation of _ElutionPeakDetection

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ElutionPeakDetection.html>`_
      -- Inherits from ['ProgressLogger', 'DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ElutionPeakDetection()
        """
        ...
    
    @overload
    def __init__(self, in_0: ElutionPeakDetection ) -> None:
        """
        Cython signature: void ElutionPeakDetection(ElutionPeakDetection &)
        """
        ...
    
    @overload
    def detectPeaks(self, in_: Kernel_MassTrace , out: List[Kernel_MassTrace] ) -> None:
        """
        Cython signature: void detectPeaks(Kernel_MassTrace & in_, libcpp_vector[Kernel_MassTrace] & out)
        """
        ...
    
    @overload
    def detectPeaks(self, in_: List[Kernel_MassTrace] , out: List[Kernel_MassTrace] ) -> None:
        """
        Cython signature: void detectPeaks(libcpp_vector[Kernel_MassTrace] & in_, libcpp_vector[Kernel_MassTrace] & out)
        """
        ...
    
    def filterByPeakWidth(self, in_: List[Kernel_MassTrace] , out: List[Kernel_MassTrace] ) -> None:
        """
        Cython signature: void filterByPeakWidth(libcpp_vector[Kernel_MassTrace] & in_, libcpp_vector[Kernel_MassTrace] & out)
        """
        ...
    
    def computeMassTraceNoise(self, in_0: Kernel_MassTrace ) -> float:
        """
        Cython signature: double computeMassTraceNoise(Kernel_MassTrace &)
        Compute noise level (as RMSE of the actual signal and the smoothed signal)
        """
        ...
    
    def computeMassTraceSNR(self, in_0: Kernel_MassTrace ) -> float:
        """
        Cython signature: double computeMassTraceSNR(Kernel_MassTrace &)
        Compute the signal to noise ratio (estimated by computeMassTraceNoise)
        """
        ...
    
    def computeApexSNR(self, in_0: Kernel_MassTrace ) -> float:
        """
        Cython signature: double computeApexSNR(Kernel_MassTrace &)
        Compute the signal to noise ratio at the apex (estimated by computeMassTraceNoise)
        """
        ...
    
    def findLocalExtrema(self, in_0: Kernel_MassTrace , in_1: int , in_2: List[int] , in_3: List[int] ) -> None:
        """
        Cython signature: void findLocalExtrema(Kernel_MassTrace &, size_t &, libcpp_vector[size_t] &, libcpp_vector[size_t] &)
        """
        ...
    
    def smoothData(self, mt: Kernel_MassTrace , win_size: int ) -> None:
        """
        Cython signature: void smoothData(Kernel_MassTrace & mt, int win_size)
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


class ExperimentalDesignFile:
    """
    Cython implementation of _ExperimentalDesignFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ExperimentalDesignFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ExperimentalDesignFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: ExperimentalDesignFile ) -> None:
        """
        Cython signature: void ExperimentalDesignFile(ExperimentalDesignFile &)
        """
        ...
    
    load: __static_ExperimentalDesignFile_load 


class FeatureDistance:
    """
    Cython implementation of _FeatureDistance

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureDistance.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, max_intensity: float , force_constraints: bool ) -> None:
        """
        Cython signature: void FeatureDistance(double max_intensity, bool force_constraints)
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureDistance ) -> None:
        """
        Cython signature: void FeatureDistance(FeatureDistance &)
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


class FeatureFinderAlgorithmMetaboIdent:
    """
    Cython implementation of _FeatureFinderAlgorithmMetaboIdent

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureFinderAlgorithmMetaboIdent.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureFinderAlgorithmMetaboIdent()
        """
        ...
    
    def setMSData(self, input: MSExperiment ) -> None:
        """
        Cython signature: void setMSData(MSExperiment & input)
        Sets spectra
        """
        ...
    
    def getMSData(self) -> MSExperiment:
        """
        Cython signature: const MSExperiment & getMSData()
        Returns spectra
        """
        ...
    
    def run(self, metaboIdentTable: List[FeatureFinderMetaboIdentCompound] , features: FeatureMap , spectra_path: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void run(const libcpp_vector[FeatureFinderMetaboIdentCompound] metaboIdentTable, FeatureMap & features, String spectra_path)
         Run feature extraction. spectra_path get's annotated as primaryMSRunPath in the resulting feature map.
        """
        ...
    
    def getChromatograms(self) -> MSExperiment:
        """
        Cython signature: MSExperiment & getChromatograms()
        Retrieves chromatograms (empty if run was not executed)
        """
        ...
    
    def getLibrary(self) -> TargetedExperiment:
        """
        Cython signature: const TargetedExperiment & getLibrary()
        Retrieves the assay library (e.g., to store as TraML, empty if run was not executed)
        """
        ...
    
    def getTransformations(self) -> TransformationDescription:
        """
        Cython signature: const TransformationDescription & getTransformations()
        Retrieves deviations between provided coordinates and extacted ones (e.g., to store as TrafoXML or for plotting)
        """
        ...
    
    def getNShared(self) -> int:
        """
        Cython signature: size_t getNShared()
        Retrieves number of features with shared identifications
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


class FeatureFinderMetaboIdentCompound:
    """
    Cython implementation of _FeatureFinderMetaboIdentCompound

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureFinderMetaboIdentCompound.html>`_
    """
    
    def __init__(self, name: Union[bytes, str, String] , formula: Union[bytes, str, String] , mass: float , charges: List[int] , rts: List[float] , rt_ranges: List[float] , iso_distrib: List[float] ) -> None:
        """
        Cython signature: void FeatureFinderMetaboIdentCompound(String name, String formula, double mass, libcpp_vector[int] charges, libcpp_vector[double] rts, libcpp_vector[double] rt_ranges, libcpp_vector[double] iso_distrib)
          Represents a compound in the in the FeatureFinderMetaboIdent library table.
        
        
          :param name: Unique name for the target compound.
          :param formula: Chemical sum formula.
          :param mass: Neutral mass; if zero calculated from formula.
          :param charges: List of possible charge states.
          :param rts: List of possible retention times.
          :param rt_ranges: List of possible retention time ranges (window around RT), either one value or one per RT entry.
          :param iso_distrib: List of relative abundances of isotopologues; if zero calculated from formula.
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
          Gets the compound name.
        
        
          :rtype: str
        """
        ...
    
    def getFormula(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFormula()
          Gets the compound chemical formula.
        
        
          :rtype: str
        """
        ...
    
    def getMass(self) -> float:
        """
        Cython signature: double getMass()
          Gets the compound mass.
        
        
          :rtype: float
        """
        ...
    
    def getCharges(self) -> List[int]:
        """
        Cython signature: libcpp_vector[int] getCharges()
          Gets the compound charge states.
        
        
          :rtype: list of int
        """
        ...
    
    def getRTs(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] getRTs()
          Gets the compound retention times.
        
        
          :rtype: list of float
        """
        ...
    
    def getRTRanges(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] getRTRanges()
          Gets the compound retention time ranges.
        
        
          :rtype: list of float
        """
        ...
    
    def getIsotopeDistribution(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] getIsotopeDistribution()
          Gets the compound isotopic distributions.
        
        
          :rtype: list of float
        """
        ... 


class GaussTraceFitter:
    """
    Cython implementation of _GaussTraceFitter

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1GaussTraceFitter.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void GaussTraceFitter()
        Fitter for RT profiles using a Gaussian background model
        """
        ...
    
    @overload
    def __init__(self, in_0: GaussTraceFitter ) -> None:
        """
        Cython signature: void GaussTraceFitter(GaussTraceFitter &)
        """
        ...
    
    def fit(self, traces: MassTraces ) -> None:
        """
        Cython signature: void fit(MassTraces & traces)
        Override important methods
        """
        ...
    
    def getLowerRTBound(self) -> float:
        """
        Cython signature: double getLowerRTBound()
        Returns the lower RT bound
        """
        ...
    
    def getUpperRTBound(self) -> float:
        """
        Cython signature: double getUpperRTBound()
        Returns the upper RT bound
        """
        ...
    
    def getHeight(self) -> float:
        """
        Cython signature: double getHeight()
        Returns height of the fitted gaussian model
        """
        ...
    
    def getCenter(self) -> float:
        """
        Cython signature: double getCenter()
        Returns center of the fitted gaussian model
        """
        ...
    
    def getFWHM(self) -> float:
        """
        Cython signature: double getFWHM()
        Returns FWHM of the fitted gaussian model
        """
        ...
    
    def getSigma(self) -> float:
        """
        Cython signature: double getSigma()
        Returns Sigma of the fitted gaussian model
        """
        ...
    
    def checkMaximalRTSpan(self, max_rt_span: float ) -> bool:
        """
        Cython signature: bool checkMaximalRTSpan(double max_rt_span)
        """
        ...
    
    def checkMinimalRTSpan(self, rt_bounds: List[float, float] , min_rt_span: float ) -> bool:
        """
        Cython signature: bool checkMinimalRTSpan(libcpp_pair[double,double] & rt_bounds, double min_rt_span)
        """
        ...
    
    def computeTheoretical(self, trace: MassTrace , k: int ) -> float:
        """
        Cython signature: double computeTheoretical(MassTrace & trace, size_t k)
        """
        ...
    
    def getArea(self) -> float:
        """
        Cython signature: double getArea()
        Returns area of the fitted gaussian model
        """
        ...
    
    def getGnuplotFormula(self, trace: MassTrace , function_name: bytes , baseline: float , rt_shift: float ) -> Union[bytes, str, String]:
        """
        Cython signature: String getGnuplotFormula(MassTrace & trace, char function_name, double baseline, double rt_shift)
        """
        ...
    
    def getValue(self, rt: float ) -> float:
        """
        Cython signature: double getValue(double rt)
        Returns value of the fitted gaussian model
        """
        ... 


class HPLC:
    """
    Cython implementation of _HPLC

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1HPLC.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void HPLC()
        Representation of a HPLC experiment
        """
        ...
    
    @overload
    def __init__(self, in_0: HPLC ) -> None:
        """
        Cython signature: void HPLC(HPLC &)
        """
        ...
    
    def getInstrument(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getInstrument()
        Returns a reference to the instument name
        """
        ...
    
    def setInstrument(self, instrument: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setInstrument(String instrument)
        Sets the instument name
        """
        ...
    
    def getColumn(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getColumn()
        Returns a reference to the column description
        """
        ...
    
    def setColumn(self, column: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setColumn(String column)
        Sets the column description
        """
        ...
    
    def getTemperature(self) -> int:
        """
        Cython signature: int getTemperature()
        Returns the temperature (in degree C)
        """
        ...
    
    def setTemperature(self, temperature: int ) -> None:
        """
        Cython signature: void setTemperature(int temperature)
        Sets the temperature (in degree C)
        """
        ...
    
    def getPressure(self) -> int:
        """
        Cython signature: unsigned int getPressure()
        Returns the pressure (in bar)
        """
        ...
    
    def setPressure(self, pressure: int ) -> None:
        """
        Cython signature: void setPressure(unsigned int pressure)
        Sets the pressure (in bar)
        """
        ...
    
    def getFlux(self) -> int:
        """
        Cython signature: unsigned int getFlux()
        Returns the flux (in microliter/sec)
        """
        ...
    
    def setFlux(self, flux: int ) -> None:
        """
        Cython signature: void setFlux(unsigned int flux)
        Sets the flux (in microliter/sec)
        """
        ...
    
    def getComment(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getComment()
        Returns the comments
        """
        ...
    
    def setComment(self, comment: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setComment(String comment)
        Sets the comments
        """
        ...
    
    def getGradient(self) -> Gradient:
        """
        Cython signature: Gradient getGradient()
        Returns a mutable reference to the used gradient
        """
        ...
    
    def setGradient(self, gradient: Gradient ) -> None:
        """
        Cython signature: void setGradient(Gradient gradient)
        Sets the used gradient
        """
        ... 


class Instrument:
    """
    Cython implementation of _Instrument

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Instrument.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Instrument()
        Description of a MS instrument
        """
        ...
    
    @overload
    def __init__(self, in_0: Instrument ) -> None:
        """
        Cython signature: void Instrument(Instrument &)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the instrument
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the name of the instrument
        """
        ...
    
    def getVendor(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVendor()
        Returns the instrument vendor
        """
        ...
    
    def setVendor(self, vendor: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setVendor(String vendor)
        Sets the instrument vendor
        """
        ...
    
    def getModel(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getModel()
        Returns the instrument model
        """
        ...
    
    def setModel(self, model: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setModel(String model)
        Sets the instrument model
        """
        ...
    
    def getCustomizations(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCustomizations()
        Returns a description of customizations
        """
        ...
    
    def setCustomizations(self, customizations: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCustomizations(String customizations)
        Sets the a description of customizations
        """
        ...
    
    def getIonSources(self) -> List[IonSource]:
        """
        Cython signature: libcpp_vector[IonSource] getIonSources()
        Returns the ion source list
        """
        ...
    
    def setIonSources(self, ion_sources: List[IonSource] ) -> None:
        """
        Cython signature: void setIonSources(libcpp_vector[IonSource] ion_sources)
        Sets the ion source list
        """
        ...
    
    def getMassAnalyzers(self) -> List[MassAnalyzer]:
        """
        Cython signature: libcpp_vector[MassAnalyzer] getMassAnalyzers()
        Returns the mass analyzer list
        """
        ...
    
    def setMassAnalyzers(self, mass_analyzers: List[MassAnalyzer] ) -> None:
        """
        Cython signature: void setMassAnalyzers(libcpp_vector[MassAnalyzer] mass_analyzers)
        Sets the mass analyzer list
        """
        ...
    
    def getIonDetectors(self) -> List[IonDetector]:
        """
        Cython signature: libcpp_vector[IonDetector] getIonDetectors()
        Returns the ion detector list
        """
        ...
    
    def setIonDetectors(self, ion_detectors: List[IonDetector] ) -> None:
        """
        Cython signature: void setIonDetectors(libcpp_vector[IonDetector] ion_detectors)
        Sets the ion detector list
        """
        ...
    
    def getSoftware(self) -> Software:
        """
        Cython signature: Software getSoftware()
        Returns the instrument software
        """
        ...
    
    def setSoftware(self, software: Software ) -> None:
        """
        Cython signature: void setSoftware(Software software)
        Sets the instrument software
        """
        ...
    
    def getIonOptics(self) -> int:
        """
        Cython signature: IonOpticsType getIonOptics()
        Returns the ion optics type
        """
        ...
    
    def setIonOptics(self, ion_optics: int ) -> None:
        """
        Cython signature: void setIonOptics(IonOpticsType ion_optics)
        Sets the ion optics type
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
    
    def __richcmp__(self, other: Instrument, op: int) -> Any:
        ... 


class IsotopeCluster:
    """
    Cython implementation of _IsotopeCluster

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsotopeCluster.html>`_
    """
    
    peaks: ChargedIndexSet
    
    scans: List[int]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IsotopeCluster()
        Stores information about an isotopic cluster (i.e. potential peptide charge variants)
        """
        ...
    
    @overload
    def __init__(self, in_0: IsotopeCluster ) -> None:
        """
        Cython signature: void IsotopeCluster(IsotopeCluster &)
        """
        ... 


class IsotopeModel:
    """
    Cython implementation of _IsotopeModel

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsotopeModel.html>`_

    Isotope distribution approximated using linear interpolation
    
    This models a smoothed (widened) distribution, i.e. can be used to sample actual raw peaks (depending on the points you query)
    If you only want the distribution (no widening), use either
    EmpiricalFormula::getIsotopeDistribution() // for a certain sum formula
    or
    IsotopeDistribution::estimateFromPeptideWeight (double average_weight)  // for averagine
    
    Peak widening is achieved by either a Gaussian or Lorentzian shape
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IsotopeModel()
        """
        ...
    
    @overload
    def __init__(self, in_0: IsotopeModel ) -> None:
        """
        Cython signature: void IsotopeModel(IsotopeModel &)
        """
        ...
    
    def getCharge(self) -> int:
        """
        Cython signature: unsigned int getCharge()
        """
        ...
    
    def setOffset(self, offset: float ) -> None:
        """
        Cython signature: void setOffset(double offset)
        Set the offset of the model
        
        The whole model will be shifted to the new offset without being computing all over
        This leaves a discrepancy which is minor in small shifts (i.e. shifting by one or two
        standard deviations) but can get significant otherwise. In that case use setParameters()
        which enforces a recomputation of the model
        """
        ...
    
    def getOffset(self) -> float:
        """
        Cython signature: double getOffset()
        Get the offset of the model
        """
        ...
    
    def getFormula(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getFormula()
        Return the Averagine peptide formula (mass calculated from mean mass and charge -- use .setParameters() to set them)
        """
        ...
    
    def setSamples(self, formula: EmpiricalFormula ) -> None:
        """
        Cython signature: void setSamples(EmpiricalFormula & formula)
        Set sample/supporting points of interpolation
        """
        ...
    
    def getCenter(self) -> float:
        """
        Cython signature: double getCenter()
        Get the center of the Isotope model
        
        This is a m/z-value not necessarily the monoisotopic mass
        """
        ...
    
    def getIsotopeDistribution(self) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution getIsotopeDistribution()
        Get the Isotope distribution (without widening) from the last setSamples() call
        
        Useful to determine the number of isotopes that the model contains and their position
        """
        ...
    Averagines : __Averagines 


class IsotopePattern:
    """
    Cython implementation of _IsotopePattern

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::FeatureFinderAlgorithmPickedHelperStructs_1_1IsotopePattern.html>`_
    """
    
    spectrum: List[int]
    
    intensity: List[float]
    
    mz_score: List[float]
    
    theoretical_mz: List[float]
    
    theoretical_pattern: TheoreticalIsotopePattern
    
    @overload
    def __init__(self, size: int ) -> None:
        """
        Cython signature: void IsotopePattern(size_t size)
        """
        ...
    
    @overload
    def __init__(self, in_0: IsotopePattern ) -> None:
        """
        Cython signature: void IsotopePattern(IsotopePattern &)
        """
        ... 


class LinearInterpolation:
    """
    Cython implementation of _LinearInterpolation[double,double]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1LinearInterpolation[double,double].html>`_

    Provides access to linearly interpolated values (and
    derivatives) from discrete data points.  Values beyond the given range
    of data points are implicitly taken as zero.
    
    The input is just a vector of values ("Data").  These are interpreted
    as the y-coordinates at the x-coordinate positions 0,...,data_.size-1.
    
    The interpolated data can also be scaled and shifted in
    the x-dimension by an affine mapping.  That is, we have "inside" and
    "outside" x-coordinates.  The affine mapping can be specified in two
    ways:
    - using setScale() and setOffset(),
    - using setMapping()
    
    By default the identity mapping (scale=1, offset=0) is used.
    
    Using the value() and derivative() methods you can sample linearly
    interpolated values for a given x-coordinate position of the data and
    the derivative of the data
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LinearInterpolation()
        """
        ...
    
    @overload
    def __init__(self, in_0: LinearInterpolation ) -> None:
        """
        Cython signature: void LinearInterpolation(LinearInterpolation &)
        """
        ...
    
    @overload
    def __init__(self, scale: float , offset: float ) -> None:
        """
        Cython signature: void LinearInterpolation(double scale, double offset)
        """
        ...
    
    def value(self, arg_pos: float ) -> float:
        """
        Cython signature: double value(double arg_pos)
        Returns the interpolated value
        """
        ...
    
    def addValue(self, arg_pos: float , arg_value: float ) -> None:
        """
        Cython signature: void addValue(double arg_pos, double arg_value)
        Performs linear resampling. The `arg_value` is split up and added to the data points around `arg_pos`
        """
        ...
    
    def derivative(self, arg_pos: float ) -> float:
        """
        Cython signature: double derivative(double arg_pos)
        Returns the interpolated derivative
        """
        ...
    
    def getData(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] getData()
        Returns the internal random access container from which interpolated values are being sampled
        """
        ...
    
    def setData(self, data: List[float] ) -> None:
        """
        Cython signature: void setData(libcpp_vector[double] & data)
        Assigns data to the internal random access container from which interpolated values are being sampled
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        Returns `true` if getData() is empty
        """
        ...
    
    def key2index(self, pos: float ) -> float:
        """
        Cython signature: double key2index(double pos)
        The transformation from "outside" to "inside" coordinates
        """
        ...
    
    def index2key(self, pos: float ) -> float:
        """
        Cython signature: double index2key(double pos)
        The transformation from "inside" to "outside" coordinates
        """
        ...
    
    def getScale(self) -> float:
        """
        Cython signature: double getScale()
        "Scale" is the difference (in "outside" units) between consecutive entries in "Data"
        """
        ...
    
    def setScale(self, scale: float ) -> None:
        """
        Cython signature: void setScale(double & scale)
        "Scale" is the difference (in "outside" units) between consecutive entries in "Data"
        """
        ...
    
    def getOffset(self) -> float:
        """
        Cython signature: double getOffset()
        "Offset" is the point (in "outside" units) which corresponds to "Data[0]"
        """
        ...
    
    def setOffset(self, offset: float ) -> None:
        """
        Cython signature: void setOffset(double & offset)
        "Offset" is the point (in "outside" units) which corresponds to "Data[0]"
        """
        ...
    
    @overload
    def setMapping(self, scale: float , inside: float , outside: float ) -> None:
        """
        Cython signature: void setMapping(double & scale, double & inside, double & outside)
        """
        ...
    
    @overload
    def setMapping(self, inside_low: float , outside_low: float , inside_high: float , outside_high: float ) -> None:
        """
        Cython signature: void setMapping(double & inside_low, double & outside_low, double & inside_high, double & outside_high)
        """
        ...
    
    def getInsideReferencePoint(self) -> float:
        """
        Cython signature: double getInsideReferencePoint()
        """
        ...
    
    def getOutsideReferencePoint(self) -> float:
        """
        Cython signature: double getOutsideReferencePoint()
        """
        ...
    
    def supportMin(self) -> float:
        """
        Cython signature: double supportMin()
        """
        ...
    
    def supportMax(self) -> float:
        """
        Cython signature: double supportMax()
        """
        ... 


class MRMAssay:
    """
    Cython implementation of _MRMAssay

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMAssay.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMAssay()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMAssay ) -> None:
        """
        Cython signature: void MRMAssay(MRMAssay &)
        """
        ...
    
    def reannotateTransitions(self, exp: TargetedExperiment , precursor_mz_threshold: float , product_mz_threshold: float , fragment_types: List[bytes] , fragment_charges: List[int] , enable_specific_losses: bool , enable_unspecific_losses: bool , round_decPow: int ) -> None:
        """
        Cython signature: void reannotateTransitions(TargetedExperiment & exp, double precursor_mz_threshold, double product_mz_threshold, libcpp_vector[String] fragment_types, libcpp_vector[size_t] fragment_charges, bool enable_specific_losses, bool enable_unspecific_losses, int round_decPow)
        Annotates and filters transitions in a TargetedExperiment
        
        
        :param exp: The input, unfiltered transitions
        :param precursor_mz_threshold: The precursor m/z threshold in Th for annotation
        :param product_mz_threshold: The product m/z threshold in Th for annotation
        :param fragment_types: The fragment types to consider for annotation
        :param fragment_charges: The fragment charges to consider for annotation
        :param enable_specific_losses: Whether specific neutral losses should be considered
        :param enable_unspecific_losses: Whether unspecific neutral losses (H2O1, H3N1, C1H2N2, C1H2N1O1) should be considered
        :param round_decPow: Round product m/z values to decimal power (default: -4)
        """
        ...
    
    def restrictTransitions(self, exp: TargetedExperiment , lower_mz_limit: float , upper_mz_limit: float , swathes: List[List[float, float]] ) -> None:
        """
        Cython signature: void restrictTransitions(TargetedExperiment & exp, double lower_mz_limit, double upper_mz_limit, libcpp_vector[libcpp_pair[double,double]] swathes)
        Restrict and filter transitions in a TargetedExperiment
        
        
        :param exp: The input, unfiltered transitions
        :param lower_mz_limit: The lower product m/z limit in Th
        :param upper_mz_limit: The upper product m/z limit in Th
        :param swathes: The swath window settings (to exclude fragment ions falling into the precursor isolation window)
        """
        ...
    
    def detectingTransitions(self, exp: TargetedExperiment , min_transitions: int , max_transitions: int ) -> None:
        """
        Cython signature: void detectingTransitions(TargetedExperiment & exp, int min_transitions, int max_transitions)
        Select detecting fragment ions
        
        
        :param exp: The input, unfiltered transitions
        :param min_transitions: The minimum number of transitions required per assay
        :param max_transitions: The maximum number of transitions required per assay
        """
        ...
    
    def filterMinMaxTransitionsCompound(self, exp: TargetedExperiment , min_transitions: int , max_transitions: int ) -> None:
        """
        Cython signature: void filterMinMaxTransitionsCompound(TargetedExperiment & exp, int min_transitions, int max_transitions)
        Filters target and decoy transitions by intensity, only keeping the top N transitions
        
        
        :param exp: The transition list which will be filtered
        :param min_transitions: The minimum number of transitions required per assay (targets only)
        :param max_transitions: The maximum number of transitions allowed per assay
        """
        ...
    
    def filterUnreferencedDecoysCompound(self, exp: TargetedExperiment ) -> None:
        """
        Cython signature: void filterUnreferencedDecoysCompound(TargetedExperiment & exp)
        Filters decoy transitions, which do not have respective target transition
        based on the transitionID.
        
        References between targets and decoys will be constructed based on the transitionsID
        and the "_decoy_" string. For example:
        
        target: 84_CompoundName_[M+H]+_88_22
        decoy: 84_CompoundName_decoy_[M+H]+_88_22
        
        
        :param exp: The transition list which will be filtered
        """
        ...
    
    def uisTransitions(self, exp: TargetedExperiment , fragment_types: List[bytes] , fragment_charges: List[int] , enable_specific_losses: bool , enable_unspecific_losses: bool , enable_ms2_precursors: bool , mz_threshold: float , swathes: List[List[float, float]] , round_decPow: int , max_num_alternative_localizations: int , shuffle_seed: int ) -> None:
        """
        Cython signature: void uisTransitions(TargetedExperiment & exp, libcpp_vector[String] fragment_types, libcpp_vector[size_t] fragment_charges, bool enable_specific_losses, bool enable_unspecific_losses, bool enable_ms2_precursors, double mz_threshold, libcpp_vector[libcpp_pair[double,double]] swathes, int round_decPow, size_t max_num_alternative_localizations, int shuffle_seed)
        Annotate UIS / site-specific transitions
        
        Performs the following actions:
        
        - Step 1: For each peptide, compute all theoretical alternative peptidoforms; see transitions generateTargetInSilicoMap_()
        - Step 2: Generate target identification transitions; see generateTargetAssays_()
        
        - Step 3a: Generate decoy sequences that share peptidoform properties with targets; see generateDecoySequences_()
        - Step 3b: Generate decoy in silico peptide map containing theoretical transition; see generateDecoyInSilicoMap_()
        - Step 4: Generate decoy identification transitions; see generateDecoyAssays_()
        
        The IPF algorithm uses the concept of "identification transitions" that
        are used to discriminate different peptidoforms, these are generated in
        this function.  In brief, the algorithm takes the existing set of
        peptides and transitions and then appends these "identification
        transitions" for targets and decoys. The novel transitions are set to be
        non-detecting and non-quantifying and are annotated with the set of
        peptidoforms to which they map.
        
        
        :param exp: The input, unfiltered transitions
        :param fragment_types: The fragment types to consider for annotation
        :param fragment_charges: The fragment charges to consider for annotation
        :param enable_specific_losses: Whether specific neutral losses should be considered
        :param enable_unspecific_losses: Whether unspecific neutral losses (H2O1, H3N1, C1H2N2, C1H2N1O1) should be considered
        :param enable_ms2_precursors: Whether MS2 precursors should be considered
        :param mz_threshold: The product m/z threshold in Th for annotation
        :param swathes: The swath window settings (to exclude fragment ions falling
        :param round_decPow: Round product m/z values to decimal power (default: -4)
        :param max_num_alternative_localizations: Maximum number of allowed peptide sequence permutations
        :param shuffle_seed: Set seed for shuffle (-1: select seed based on time)
        :param disable_decoy_transitions: Whether to disable generation of decoy UIS transitions
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


class MRMFeatureFinderScoring:
    """
    Cython implementation of _MRMFeatureFinderScoring

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMFeatureFinderScoring.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void MRMFeatureFinderScoring()
        """
        ...
    
    def pickExperiment(self, chromatograms: MSExperiment , output: FeatureMap , transition_exp_: TargetedExperiment , trafo: TransformationDescription , swath_map: MSExperiment ) -> None:
        """
        Cython signature: void pickExperiment(MSExperiment & chromatograms, FeatureMap & output, TargetedExperiment & transition_exp_, TransformationDescription trafo, MSExperiment & swath_map)
        Pick features in one experiment containing chromatogram
        
        Function for for wrapping in Python, only uses OpenMS datastructures and does not return the map
        
        
        :param chromatograms: The input chromatograms
        :param output: The output features with corresponding scores
        :param transition_exp: The transition list describing the experiment
        :param trafo: Optional transformation of the experimental retention time to the normalized retention time space used in the transition list
        :param swath_map: Optional SWATH-MS (DIA) map corresponding from which the chromatograms were extracted
        """
        ...
    
    def setStrictFlag(self, flag: bool ) -> None:
        """
        Cython signature: void setStrictFlag(bool flag)
        """
        ...
    
    @overload
    def setMS1Map(self, ms1_map: SpectrumAccessOpenMS ) -> None:
        """
        Cython signature: void setMS1Map(shared_ptr[SpectrumAccessOpenMS] ms1_map)
        """
        ...
    
    @overload
    def setMS1Map(self, ms1_map: SpectrumAccessOpenMSCached ) -> None:
        """
        Cython signature: void setMS1Map(shared_ptr[SpectrumAccessOpenMSCached] ms1_map)
        """
        ...
    
    def scorePeakgroups(self, transition_group: LightMRMTransitionGroupCP , trafo: TransformationDescription , swath_maps: List[SwathMap] , output: FeatureMap , ms1only: bool ) -> None:
        """
        Cython signature: void scorePeakgroups(LightMRMTransitionGroupCP transition_group, TransformationDescription trafo, libcpp_vector[SwathMap] swath_maps, FeatureMap & output, bool ms1only)
        Score all peak groups of a transition group
        
        Iterate through all features found along the chromatograms of the transition group and score each one individually
        
        
        :param transition_group: The MRMTransitionGroup to be scored (input)
        :param trafo: Optional transformation of the experimental retention time
            to the normalized retention time space used in thetransition list
        :param swath_maps: Optional SWATH-MS (DIA) map corresponding from which
            the chromatograms were extracted. Use empty map if no data is available
        :param output: The output features with corresponding scores (the found
            features will be added to this FeatureMap)
        :param ms1only: Whether to only do MS1 scoring and skip all MS2 scoring
        """
        ...
    
    def prepareProteinPeptideMaps_(self, transition_exp: LightTargetedExperiment ) -> None:
        """
        Cython signature: void prepareProteinPeptideMaps_(LightTargetedExperiment & transition_exp)
        Prepares the internal mappings of peptides and proteins
        
        Calling this method _is_ required before calling scorePeakgroups
        
        
        :param transition_exp: The transition list describing the experiment
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


class MRMFeatureQCFile:
    """
    Cython implementation of _MRMFeatureQCFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMFeatureQCFile.html>`_

    File adapter for MRMFeatureQC files
    
    Loads and stores .csv or .tsv files describing an MRMFeatureQC
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMFeatureQCFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMFeatureQCFile ) -> None:
        """
        Cython signature: void MRMFeatureQCFile(MRMFeatureQCFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , mrmfqc: MRMFeatureQC , is_component_group: bool ) -> None:
        """
        Cython signature: void load(const String & filename, MRMFeatureQC & mrmfqc, const bool is_component_group)
        Loads an MRMFeatureQC file
        
        
        :param filename: The path to the input file
        :param mrmfqc: The output class which will contain the criteria
        :param is_component_group: True if the user intends to load ComponentGroupQCs data, false otherwise
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ... 


class MRMTransitionGroupPicker:
    """
    Cython implementation of _MRMTransitionGroupPicker

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMTransitionGroupPicker.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMTransitionGroupPicker()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMTransitionGroupPicker ) -> None:
        """
        Cython signature: void MRMTransitionGroupPicker(MRMTransitionGroupPicker &)
        """
        ...
    
    @overload
    def pickTransitionGroup(self, transition_group: LightMRMTransitionGroupCP ) -> None:
        """
        Cython signature: void pickTransitionGroup(LightMRMTransitionGroupCP transition_group)
        """
        ...
    
    @overload
    def pickTransitionGroup(self, transition_group: MRMTransitionGroupCP ) -> None:
        """
        Cython signature: void pickTransitionGroup(MRMTransitionGroupCP transition_group)
        """
        ...
    
    def createMRMFeature(self, transition_group: LightMRMTransitionGroupCP , picked_chroms: List[MSChromatogram] , smoothed_chroms: List[MSChromatogram] , chr_idx: int , peak_idx: int ) -> MRMFeature:
        """
        Cython signature: MRMFeature createMRMFeature(LightMRMTransitionGroupCP transition_group, libcpp_vector[MSChromatogram] & picked_chroms, libcpp_vector[MSChromatogram] & smoothed_chroms, const int chr_idx, const int peak_idx)
        """
        ...
    
    def remove_overlapping_features(self, picked_chroms: List[MSChromatogram] , best_left: float , best_right: float ) -> None:
        """
        Cython signature: void remove_overlapping_features(libcpp_vector[MSChromatogram] & picked_chroms, double best_left, double best_right)
        """
        ...
    
    def findLargestPeak(self, picked_chroms: List[MSChromatogram] , chr_idx: int , peak_idx: int ) -> None:
        """
        Cython signature: void findLargestPeak(libcpp_vector[MSChromatogram] & picked_chroms, int & chr_idx, int & peak_idx)
        """
        ...
    
    def findWidestPeakIndices(self, picked_chroms: List[MSChromatogram] , chrom_idx: int , point_idx: int ) -> None:
        """
        Cython signature: void findWidestPeakIndices(libcpp_vector[MSChromatogram] & picked_chroms, int & chrom_idx, int & point_idx)
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


class MZTrafoModel:
    """
    Cython implementation of _MZTrafoModel

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MZTrafoModel.html>`_

    Create and apply models of a mass recalibration function
    
    The input is a list of calibration points (ideally spanning a wide m/z range to prevent extrapolation when applying to model)
    
    Models (LINEAR, LINEAR_WEIGHTED, QUADRATIC, QUADRATIC_WEIGHTED) can be trained using CalData points (or a subset of them)
    Calibration points can have different retention time points, and a model should be build such that it captures
    the local (in time) decalibration of the instrument, i.e. choose appropriate time windows along RT to calibrate the
    spectra in this RT region
    From the available calibrant data, a model is build. Later, any uncalibrated m/z value can be fed to the model, to obtain
    a calibrated m/z
    
    The input domain can either be absolute mass differences in [Th], or relative differences in [ppm]
    The models are build based on this input
    
    Outlier detection before model building via the RANSAC algorithm is supported for LINEAR and QUADRATIC models
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MZTrafoModel()
        """
        ...
    
    @overload
    def __init__(self, in_0: MZTrafoModel ) -> None:
        """
        Cython signature: void MZTrafoModel(MZTrafoModel &)
        """
        ...
    
    @overload
    def __init__(self, in_0: bool ) -> None:
        """
        Cython signature: void MZTrafoModel(bool)
        """
        ...
    
    def isTrained(self) -> bool:
        """
        Cython signature: bool isTrained()
        Returns true if the model have coefficients (i.e. was trained successfully)
        """
        ...
    
    def getRT(self) -> float:
        """
        Cython signature: double getRT()
        Get RT associated with the model (training region)
        """
        ...
    
    def predict(self, mz: float ) -> float:
        """
        Cython signature: double predict(double mz)
        Apply the model to an uncalibrated m/z value
        
        Make sure the model was trained (train()) and is valid (isValidModel()) before calling this function!
        
        Applies the function y = intercept + slope*mz + power*mz^2
        and returns y
        
        
        :param mz: The uncalibrated m/z value
        :return: The calibrated m/z value
        """
        ...
    
    @overload
    def train(self, cd: CalibrationData , md: int , use_RANSAC: bool , rt_left: float , rt_right: float ) -> bool:
        """
        Cython signature: bool train(CalibrationData cd, MZTrafoModel_MODELTYPE md, bool use_RANSAC, double rt_left, double rt_right)
        Train a model using calibrant data
        
        If the CalibrationData was created using peak groups (usually corresponding to mass traces),
        the median for each group is used as a group representative. This
        is more robust, and reduces the number of data points drastically, i.e. one value per group
        
        Internally, these steps take place:
        - apply RT filter
        - [compute median per group] (only if groups were given in 'cd')
        - set Model's rt position
        - call train() (see overloaded method)
        
        
        :param cd: List of calibrants
        :param md: Type of model (linear, quadratic, ...)
        :param use_RANSAC: Remove outliers before computing the model?
        :param rt_left: Filter 'cd' by RT; all calibrants with RT < 'rt_left' are removed
        :param rt_right: Filter 'cd' by RT; all calibrants with RT > 'rt_right' are removed
        :return: True if model was build, false otherwise
        """
        ...
    
    @overload
    def train(self, error_mz: List[float] , theo_mz: List[float] , weights: List[float] , md: int , use_RANSAC: bool ) -> bool:
        """
        Cython signature: bool train(libcpp_vector[double] error_mz, libcpp_vector[double] theo_mz, libcpp_vector[double] weights, MZTrafoModel_MODELTYPE md, bool use_RANSAC)
        Train a model using calibrant data
        
        Given theoretical and observed mass values (and corresponding weights),
        a model (linear, quadratic, ...) is build
        Outlier removal is applied before
        The 'obs_mz' can be either given as absolute masses in [Th] or relative deviations in [ppm]
        The MZTrafoModel must be constructed accordingly (see constructor). This has no influence on the model building itself, but
        rather on how 'predict()' works internally
        
        Outlier detection before model building via the RANSAC algorithm is supported for LINEAR and QUADRATIC models
        
        Internally, these steps take place:
        - [apply RANSAC] (depending on 'use_RANSAC')
        - build model and store its parameters internally
        
        
        :param error_mz: Observed Mass error (in ppm or Th)
        :param theo_mz: Theoretical m/z values, corresponding to 'error_mz'
        :param weights: For weighted models only: weight of calibrants; ignored otherwise
        :param md: Type of model (linear, quadratic, ...)
        :param use_RANSAC: Remove outliers before computing the model?
        :return: True if model was build, false otherwise
        """
        ...
    
    def getCoefficients(self, intercept: float , slope: float , power: float ) -> None:
        """
        Cython signature: void getCoefficients(double & intercept, double & slope, double & power)
        Get model coefficients
        
        Parameters will be filled with internal model parameters
        The model must be trained before; Exception is thrown otherwise!
        
        
        :param intercept: The intercept
        :param slope: The slope
        :param power: The coefficient for x*x (will be 0 for linear models)
        """
        ...
    
    @overload
    def setCoefficients(self, in_0: MZTrafoModel ) -> None:
        """
        Cython signature: void setCoefficients(MZTrafoModel)
        Copy model coefficients from another model
        """
        ...
    
    @overload
    def setCoefficients(self, in_0: float , in_1: float , in_2: float ) -> None:
        """
        Cython signature: void setCoefficients(double, double, double)
        Manually set model coefficients
        
        Can be used instead of train(), so manually set coefficients
        It must be exactly three values. If you want a linear model, set 'power' to zero
        If you want a constant model, set slope to zero in addition
        
        
        :param intercept: The offset
        :param slope: The slope
        :param power: The x*x coefficient (for quadratic models)
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
    
    enumToName: __static_MZTrafoModel_enumToName
    
    findNearest: __static_MZTrafoModel_findNearest
    
    isValidModel: __static_MZTrafoModel_isValidModel
    
    nameToEnum: __static_MZTrafoModel_nameToEnum
    
    setCoefficientLimits: __static_MZTrafoModel_setCoefficientLimits
    
    setRANSACParams: __static_MZTrafoModel_setRANSACParams 


class MassTrace:
    """
    Cython implementation of _MassTrace

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::FeatureFinderAlgorithmPickedHelperStructs_1_1MassTrace.html>`_
    """
    
    max_rt: float
    
    theoretical_int: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MassTrace()
        """
        ...
    
    @overload
    def __init__(self, in_0: MassTrace ) -> None:
        """
        Cython signature: void MassTrace(MassTrace &)
        """
        ...
    
    def getConvexhull(self) -> ConvexHull2D:
        """
        Cython signature: ConvexHull2D getConvexhull()
        """
        ...
    
    def updateMaximum(self) -> None:
        """
        Cython signature: void updateMaximum()
        """
        ...
    
    def getAvgMZ(self) -> float:
        """
        Cython signature: double getAvgMZ()
        """
        ...
    
    def isValid(self) -> bool:
        """
        Cython signature: bool isValid()
        """
        ... 


class MassTraces:
    """
    Cython implementation of _MassTraces

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::FeatureFinderAlgorithmPickedHelperStructs_1_1MassTraces.html>`_
    """
    
    max_trace: int
    
    baseline: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MassTraces()
        """
        ...
    
    @overload
    def __init__(self, in_0: MassTraces ) -> None:
        """
        Cython signature: void MassTraces(MassTraces &)
        """
        ...
    
    def getPeakCount(self) -> int:
        """
        Cython signature: size_t getPeakCount()
        """
        ...
    
    def isValid(self, seed_mz: float , trace_tolerance: float ) -> bool:
        """
        Cython signature: bool isValid(double seed_mz, double trace_tolerance)
        """
        ...
    
    def getTheoreticalmaxPosition(self) -> int:
        """
        Cython signature: size_t getTheoreticalmaxPosition()
        """
        ...
    
    def updateBaseline(self) -> None:
        """
        Cython signature: void updateBaseline()
        """
        ...
    
    def getRTBounds(self) -> List[float, float]:
        """
        Cython signature: libcpp_pair[double,double] getRTBounds()
        """
        ... 


class MetaInfoDescription:
    """
    Cython implementation of _MetaInfoDescription

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaInfoDescription.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaInfoDescription()
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaInfoDescription ) -> None:
        """
        Cython signature: void MetaInfoDescription(MetaInfoDescription &)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the peak annotations
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the name of the peak annotations
        """
        ...
    
    def getDataProcessing(self) -> List[DataProcessing]:
        """
        Cython signature: libcpp_vector[shared_ptr[DataProcessing]] getDataProcessing()
        Returns a reference to the description of the applied processing
        """
        ...
    
    def setDataProcessing(self, in_0: List[DataProcessing] ) -> None:
        """
        Cython signature: void setDataProcessing(libcpp_vector[shared_ptr[DataProcessing]])
        Sets the description of the applied processing
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
    
    def __richcmp__(self, other: MetaInfoDescription, op: int) -> Any:
        ... 


class ModificationDefinitionsSet:
    """
    Cython implementation of _ModificationDefinitionsSet

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ModificationDefinitionsSet.html>`_

    Representation of a set of modification definitions
    
    This class enhances the modification definitions as defined in the
    class ModificationDefinition into a set of definitions. This is also
    e.g. used as input parameters in search engines.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ModificationDefinitionsSet()
        """
        ...
    
    @overload
    def __init__(self, in_0: ModificationDefinitionsSet ) -> None:
        """
        Cython signature: void ModificationDefinitionsSet(ModificationDefinitionsSet &)
        """
        ...
    
    @overload
    def __init__(self, fixed_modifications: List[bytes] , variable_modifications: List[bytes] ) -> None:
        """
        Cython signature: void ModificationDefinitionsSet(StringList fixed_modifications, StringList variable_modifications)
        """
        ...
    
    def setMaxModifications(self, max_mod: int ) -> None:
        """
        Cython signature: void setMaxModifications(size_t max_mod)
        Sets the maximal number of modifications allowed per peptide
        """
        ...
    
    def getMaxModifications(self) -> int:
        """
        Cython signature: size_t getMaxModifications()
        Return the maximal number of modifications allowed per peptide
        """
        ...
    
    def getNumberOfModifications(self) -> int:
        """
        Cython signature: size_t getNumberOfModifications()
        Returns the number of modifications stored in this set
        """
        ...
    
    def getNumberOfFixedModifications(self) -> int:
        """
        Cython signature: size_t getNumberOfFixedModifications()
        Returns the number of fixed modifications stored in this set
        """
        ...
    
    def getNumberOfVariableModifications(self) -> int:
        """
        Cython signature: size_t getNumberOfVariableModifications()
        Returns the number of variable modifications stored in this set
        """
        ...
    
    def addModification(self, mod_def: ModificationDefinition ) -> None:
        """
        Cython signature: void addModification(ModificationDefinition & mod_def)
        Adds a modification definition to the set
        """
        ...
    
    @overload
    def setModifications(self, mod_defs: Set[ModificationDefinition] ) -> None:
        """
        Cython signature: void setModifications(libcpp_set[ModificationDefinition] & mod_defs)
        Sets the modification definitions
        """
        ...
    
    @overload
    def setModifications(self, fixed_modifications: Union[bytes, str, String] , variable_modifications: String ) -> None:
        """
        Cython signature: void setModifications(const String & fixed_modifications, String & variable_modifications)
        Set the modification definitions from a string
        
        The strings should contain a comma separated list of modifications. The names
        can be PSI-MOD identifier or any other unique name supported by PSI-MOD. TermSpec
        definitions and other specific definitions are given by the modifications themselves.
        """
        ...
    
    @overload
    def setModifications(self, fixed_modifications: List[bytes] , variable_modifications: List[bytes] ) -> None:
        """
        Cython signature: void setModifications(StringList & fixed_modifications, StringList & variable_modifications)
        Same as above, but using StringList instead of comma separated strings
        """
        ...
    
    def getModifications(self) -> Set[ModificationDefinition]:
        """
        Cython signature: libcpp_set[ModificationDefinition] getModifications()
        Returns the stored modification definitions
        """
        ...
    
    def getFixedModifications(self) -> Set[ModificationDefinition]:
        """
        Cython signature: libcpp_set[ModificationDefinition] getFixedModifications()
        Returns the stored fixed modification definitions
        """
        ...
    
    def getVariableModifications(self) -> Set[ModificationDefinition]:
        """
        Cython signature: libcpp_set[ModificationDefinition] getVariableModifications()
        Returns the stored variable modification definitions
        """
        ...
    
    @overload
    def getModificationNames(self, fixed_modifications: List[bytes] , variable_modifications: List[bytes] ) -> None:
        """
        Cython signature: void getModificationNames(StringList & fixed_modifications, StringList & variable_modifications)
        Populates the output lists with the modification names (use e.g. for
        """
        ...
    
    @overload
    def getModificationNames(self, ) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getModificationNames()
        Returns only the names of the modifications stored in the set
        """
        ...
    
    def getFixedModificationNames(self) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getFixedModificationNames()
        Returns only the names of the fixed modifications
        """
        ...
    
    def getVariableModificationNames(self) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getVariableModificationNames()
        Returns only the names of the variable modifications
        """
        ...
    
    def isCompatible(self, peptide: AASequence ) -> bool:
        """
        Cython signature: bool isCompatible(AASequence & peptide)
        Returns true if the peptide is compatible with the definitions, e.g. does not contain other modifications
        """
        ...
    
    def inferFromPeptides(self, peptides: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void inferFromPeptides(libcpp_vector[PeptideIdentification] & peptides)
        Infers the sets of defined modifications from the modifications present on peptide identifications
        """
        ... 


class ModificationsDB:
    """
    Cython implementation of _ModificationsDB

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ModificationsDB.html>`_
    """
    
    def getNumberOfModifications(self) -> int:
        """
        Cython signature: size_t getNumberOfModifications()
        Returns the number of modifications read from the unimod.xml file
        """
        ...
    
    def searchModifications(self, mods: Set[ResidueModification] , mod_name: Union[bytes, str, String] , residue: Union[bytes, str, String] , term_spec: int ) -> None:
        """
        Cython signature: void searchModifications(libcpp_set[const ResidueModification *] & mods, const String & mod_name, const String & residue, TermSpecificity term_spec)
        Collects all modifications which have the given name as synonym
        
        If `residue` is set, only modifications with matching residue of origin are considered
        If `term_spec` is set, only modifications with matching term specificity are considered
        The resulting set of modifications will be empty if no modification exists that fulfills the criteria
        """
        ...
    
    @overload
    def getModification(self, index: int ) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getModification(size_t index)
        Returns the modification with the given index
        """
        ...
    
    @overload
    def getModification(self, mod_name: Union[bytes, str, String] ) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getModification(const String & mod_name)
        Returns the modification with the given name
        """
        ...
    
    @overload
    def getModification(self, mod_name: Union[bytes, str, String] , residue: Union[bytes, str, String] , term_spec: int ) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getModification(const String & mod_name, const String & residue, TermSpecificity term_spec)
        Returns the modification with the given arguments
        """
        ...
    
    def has(self, modification: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool has(String modification)
        Returns true if the modification exists
        """
        ...
    
    def addModification(self, new_mod: ResidueModification ) -> ResidueModification:
        """
        Cython signature: const ResidueModification * addModification(const ResidueModification & new_mod)
        Add a new modification to ModificationsDB. If the modification already exists (based on its fullID) it is not added. Returns the modification in the ModificationDB (which can differ from input if mod was already present).
        """
        ...
    
    def findModificationIndex(self, mod_name: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t findModificationIndex(const String & mod_name)
        Returns the index of the modification in the mods_ vector; a unique name must be given
        """
        ...
    
    def searchModificationsByDiffMonoMass(self, mods: List[bytes] , mass: float , max_error: float , residue: Union[bytes, str, String] , term_spec: int ) -> None:
        """
        Cython signature: void searchModificationsByDiffMonoMass(libcpp_vector[String] & mods, double mass, double max_error, const String & residue, TermSpecificity term_spec)
        Collects all modifications with delta mass inside a tolerance window
        """
        ...
    
    def getBestModificationByDiffMonoMass(self, mass: float , max_error: float , residue: Union[bytes, str, String] , term_spec: int ) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getBestModificationByDiffMonoMass(double mass, double max_error, const String & residue, TermSpecificity term_spec)
        Returns the best matching modification for the given delta mass and residue
        
        Query the modifications DB to get the best matching modification with
        the given delta mass at the given residue (NULL pointer means no result,
        maybe the maximal error tolerance needs to be increased). Possible
        input for CAM modification would be a delta mass of 57 and a residue
        of "C".
        
        Note: If there are multiple possible matches with equal masses, it
        will choose the _first_ match which defaults to the first matching
        UniMod entry.
        
        
        :param residue: The residue at which the modifications occurs
        :param mass: The monoisotopic mass of the residue including the mass of the modification
        :param max_error: The maximal mass error in the modification search
        :return: A pointer to the best matching modification (or NULL if none was found)
        """
        ...
    
    def getAllSearchModifications(self, modifications: List[bytes] ) -> None:
        """
        Cython signature: void getAllSearchModifications(libcpp_vector[String] & modifications)
        Collects all modifications that can be used for identification searches
        """
        ...
    
    def isInstantiated(self) -> bool:
        """
        Cython signature: bool isInstantiated()
        Check whether ModificationsDB was instantiated before
        """
        ... 


class MorpheusScore:
    """
    Cython implementation of _MorpheusScore

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MorpheusScore.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MorpheusScore()
        """
        ...
    
    @overload
    def __init__(self, in_0: MorpheusScore ) -> None:
        """
        Cython signature: void MorpheusScore(MorpheusScore &)
        """
        ...
    
    def compute(self, fragment_mass_tolerance: float , fragment_mass_tolerance_unit_ppm: bool , exp_spectrum: MSSpectrum , theo_spectrum: MSSpectrum ) -> MorpheusScore_Result:
        """
        Cython signature: MorpheusScore_Result compute(double fragment_mass_tolerance, bool fragment_mass_tolerance_unit_ppm, const MSSpectrum & exp_spectrum, const MSSpectrum & theo_spectrum)
        Returns Morpheus Score
        """
        ... 


class MorpheusScore_Result:
    """
    Cython implementation of _MorpheusScore_Result

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MorpheusScore_Result.html>`_
    """
    
    matches: int
    
    n_peaks: int
    
    score: float
    
    MIC: float
    
    TIC: float
    
    err: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MorpheusScore_Result()
        """
        ...
    
    @overload
    def __init__(self, in_0: MorpheusScore_Result ) -> None:
        """
        Cython signature: void MorpheusScore_Result(MorpheusScore_Result &)
        """
        ... 


class OSSpectrumMeta:
    """
    Cython implementation of _OSSpectrumMeta

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1OSSpectrumMeta.html>`_
    """
    
    index: int
    
    id: bytes
    
    RT: float
    
    ms_level: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OSSpectrumMeta()
        """
        ...
    
    @overload
    def __init__(self, in_0: OSSpectrumMeta ) -> None:
        """
        Cython signature: void OSSpectrumMeta(OSSpectrumMeta &)
        """
        ... 


class OSWFile:
    """
    Cython implementation of _OSWFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OSWFile.html>`_

    This class serves for reading in and writing OpenSWATH OSW files
    
    See OpenSwathOSWWriter for more functionality
    
    The reader and writer returns data in a format suitable for PercolatorAdapter.
    OSW files have a flexible data structure. They contain all peptide query
    parameters of TraML/PQP files with the detected and quantified features of
    OpenSwathWorkflow (feature, feature_ms1, feature_ms2 & feature_transition)
    
    The OSWFile reader extracts the feature information from the OSW file for
    each level (MS1, MS2 & transition) separately and generates Percolator input
    files. For each of the three Percolator reports, OSWFile writer adds a table
    (score_ms1, score_ms2, score_transition) with the respective confidence metrics.
    These tables can be mapped to the corresponding feature tables, are very similar
    to PyProphet results and can thus be used interchangeably
    """
    
    @overload
    def __init__(self, filename: Union[bytes, str] ) -> None:
        """
        Cython signature: void OSWFile(const libcpp_utf8_string filename)
        """
        ...
    
    @overload
    def __init__(self, in_0: OSWFile ) -> None:
        """
        Cython signature: void OSWFile(OSWFile &)
        """
        ... 


class ParamValue:
    """
    Cython implementation of _ParamValue

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ParamValue.html>`_

    Class to hold strings, numeric values, vectors of strings and vectors of numeric values using the stl types
    
    - To choose one of these types, just use the appropriate constructor
    - Automatic conversion is supported and throws Exceptions in case of invalid conversions
    - An empty object is created with the default constructor
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ParamValue()
        """
        ...
    
    @overload
    def __init__(self, in_0: ParamValue ) -> None:
        """
        Cython signature: void ParamValue(ParamValue &)
        """
        ...
    
    @overload
    def __init__(self, in_0: bytes ) -> None:
        """
        Cython signature: void ParamValue(char *)
        """
        ...
    
    @overload
    def __init__(self, in_0: Union[bytes, str] ) -> None:
        """
        Cython signature: void ParamValue(const libcpp_utf8_string &)
        """
        ...
    
    @overload
    def __init__(self, in_0: int ) -> None:
        """
        Cython signature: void ParamValue(int)
        """
        ...
    
    @overload
    def __init__(self, in_0: float ) -> None:
        """
        Cython signature: void ParamValue(double)
        """
        ...
    
    @overload
    def __init__(self, in_0: List[Union[bytes, str]] ) -> None:
        """
        Cython signature: void ParamValue(libcpp_vector[libcpp_utf8_string])
        """
        ...
    
    @overload
    def __init__(self, in_0: List[int] ) -> None:
        """
        Cython signature: void ParamValue(libcpp_vector[int])
        """
        ...
    
    @overload
    def __init__(self, in_0: List[float] ) -> None:
        """
        Cython signature: void ParamValue(libcpp_vector[double])
        """
        ...
    
    def toStringVector(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[libcpp_string] toStringVector()
        Explicitly convert ParamValue to string vector
        """
        ...
    
    def toDoubleVector(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] toDoubleVector()
        Explicitly convert ParamValue to DoubleList
        """
        ...
    
    def toIntVector(self) -> List[int]:
        """
        Cython signature: libcpp_vector[int] toIntVector()
        Explicitly convert ParamValue to IntList
        """
        ...
    
    def toBool(self) -> bool:
        """
        Cython signature: bool toBool()
        Converts the strings 'true' and 'false' to a bool
        """
        ...
    
    def valueType(self) -> int:
        """
        Cython signature: ValueType valueType()
        """
        ...
    
    def isEmpty(self) -> int:
        """
        Cython signature: int isEmpty()
        Test if the value is empty
        """
        ... 


class ParamXMLFile:
    """
    Cython implementation of _ParamXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ParamXMLFile.html>`_

    The file pendant of the Param class used to load and store the param
    datastructure as paramXML
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ParamXMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: ParamXMLFile ) -> None:
        """
        Cython signature: void ParamXMLFile(ParamXMLFile &)
        """
        ...
    
    def load(self, in_0: Union[bytes, str, String] , in_1: Param ) -> None:
        """
        Cython signature: void load(String, Param &)
        Read XML file
        
        
        :param filename: The file from where to read the Param object
        :param param: The param object where the read data should be stored
        :raises:
          Exception: FileNotFound is thrown if the file could not be found
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ...
    
    def store(self, in_0: Union[bytes, str, String] , in_1: Param ) -> None:
        """
        Cython signature: void store(String, Param &)
        Write XML file
        
        
        :param filename: The filename where the param data structure should be stored
        :param param: The Param class that should be stored in the file
        """
        ... 


class PeakFileOptions:
    """
    Cython implementation of _PeakFileOptions

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeakFileOptions.html>`_

    Options for loading files containing peak data
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeakFileOptions()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeakFileOptions ) -> None:
        """
        Cython signature: void PeakFileOptions(PeakFileOptions &)
        """
        ...
    
    def setMetadataOnly(self, in_0: bool ) -> None:
        """
        Cython signature: void setMetadataOnly(bool)
        Sets whether or not to load only meta data
        """
        ...
    
    def getMetadataOnly(self) -> bool:
        """
        Cython signature: bool getMetadataOnly()
        Returns whether or not to load only meta data
        """
        ...
    
    def setWriteSupplementalData(self, in_0: bool ) -> None:
        """
        Cython signature: void setWriteSupplementalData(bool)
        Sets whether or not to write supplemental peak data in MzData files
        """
        ...
    
    def getWriteSupplementalData(self) -> bool:
        """
        Cython signature: bool getWriteSupplementalData()
        Returns whether or not to write supplemental peak data in MzData files
        """
        ...
    
    def setMSLevels(self, levels: List[int] ) -> None:
        """
        Cython signature: void setMSLevels(libcpp_vector[int] levels)
        Sets the desired MS levels for peaks to load
        """
        ...
    
    def addMSLevel(self, level: int ) -> None:
        """
        Cython signature: void addMSLevel(int level)
        Adds a desired MS level for peaks to load
        """
        ...
    
    def clearMSLevels(self) -> None:
        """
        Cython signature: void clearMSLevels()
        Clears the MS levels
        """
        ...
    
    def hasMSLevels(self) -> bool:
        """
        Cython signature: bool hasMSLevels()
        Returns true, if MS levels have been set
        """
        ...
    
    def containsMSLevel(self, level: int ) -> bool:
        """
        Cython signature: bool containsMSLevel(int level)
        Returns true, if MS level `level` has been set
        """
        ...
    
    def getMSLevels(self) -> List[int]:
        """
        Cython signature: libcpp_vector[int] getMSLevels()
        Returns the set MS levels
        """
        ...
    
    def setCompression(self, in_0: bool ) -> None:
        """
        Cython signature: void setCompression(bool)
        Sets if data should be compressed when writing
        """
        ...
    
    def getCompression(self) -> bool:
        """
        Cython signature: bool getCompression()
        Returns true, if data should be compressed when writing
        """
        ...
    
    def setMz32Bit(self, mz_32_bit: bool ) -> None:
        """
        Cython signature: void setMz32Bit(bool mz_32_bit)
        Sets if mz-data and rt-data should be stored with 32bit or 64bit precision
        """
        ...
    
    def getMz32Bit(self) -> bool:
        """
        Cython signature: bool getMz32Bit()
        Returns true, if mz-data and rt-data should be stored with 32bit precision
        """
        ...
    
    def setIntensity32Bit(self, int_32_bit: bool ) -> None:
        """
        Cython signature: void setIntensity32Bit(bool int_32_bit)
        Sets if intensity data should be stored with 32bit or 64bit precision
        """
        ...
    
    def getIntensity32Bit(self) -> bool:
        """
        Cython signature: bool getIntensity32Bit()
        Returns true, if intensity data should be stored with 32bit precision
        """
        ...
    
    def setRTRange(self, range_: DRange1 ) -> None:
        """
        Cython signature: void setRTRange(DRange1 & range_)
        Restricts the range of RT values for peaks to load
        """
        ...
    
    def hasRTRange(self) -> bool:
        """
        Cython signature: bool hasRTRange()
        Returns true if an RT range has been set
        """
        ...
    
    def getRTRange(self) -> DRange1:
        """
        Cython signature: DRange1 getRTRange()
        Returns the RT range
        """
        ...
    
    def setMZRange(self, range_: DRange1 ) -> None:
        """
        Cython signature: void setMZRange(DRange1 & range_)
        Restricts the range of MZ values for peaks to load
        """
        ...
    
    def hasMZRange(self) -> bool:
        """
        Cython signature: bool hasMZRange()
        Returns true if an MZ range has been set
        """
        ...
    
    def getMZRange(self) -> DRange1:
        """
        Cython signature: DRange1 getMZRange()
        Returns the MZ range
        """
        ...
    
    def setIntensityRange(self, range_: DRange1 ) -> None:
        """
        Cython signature: void setIntensityRange(DRange1 & range_)
        Restricts the range of intensity values for peaks to load
        """
        ...
    
    def hasIntensityRange(self) -> bool:
        """
        Cython signature: bool hasIntensityRange()
        Returns true if an intensity range has been set
        """
        ...
    
    def getIntensityRange(self) -> DRange1:
        """
        Cython signature: DRange1 getIntensityRange()
        Returns the intensity range
        """
        ...
    
    def getMaxDataPoolSize(self) -> int:
        """
        Cython signature: size_t getMaxDataPoolSize()
        Returns maximal size of the data pool
        """
        ...
    
    def setMaxDataPoolSize(self, s: int ) -> None:
        """
        Cython signature: void setMaxDataPoolSize(size_t s)
        Sets maximal size of the data pool
        """
        ...
    
    def setSortSpectraByMZ(self, doSort: bool ) -> None:
        """
        Cython signature: void setSortSpectraByMZ(bool doSort)
        Sets whether or not to sort peaks in spectra
        """
        ...
    
    def getSortSpectraByMZ(self) -> bool:
        """
        Cython signature: bool getSortSpectraByMZ()
        Returns whether or not peaks in spectra should be sorted
        """
        ...
    
    def setSortChromatogramsByRT(self, doSort: bool ) -> None:
        """
        Cython signature: void setSortChromatogramsByRT(bool doSort)
        Sets whether or not to sort peaks in chromatograms
        """
        ...
    
    def getSortChromatogramsByRT(self) -> bool:
        """
        Cython signature: bool getSortChromatogramsByRT()
        Returns whether or not peaks in chromatograms should be sorted
        """
        ...
    
    def hasFilters(self) -> bool:
        """
        Cython signature: bool hasFilters()
        """
        ...
    
    def setFillData(self, only: bool ) -> None:
        """
        Cython signature: void setFillData(bool only)
        Sets whether to fill the actual data into the container (spectrum/chromatogram)
        """
        ...
    
    def getFillData(self) -> bool:
        """
        Cython signature: bool getFillData()
        Returns whether to fill the actual data into the container (spectrum/chromatogram)
        """
        ...
    
    def setSkipXMLChecks(self, only: bool ) -> None:
        """
        Cython signature: void setSkipXMLChecks(bool only)
        Sets whether to skip some XML checks and be fast instead
        """
        ...
    
    def getSkipXMLChecks(self) -> bool:
        """
        Cython signature: bool getSkipXMLChecks()
        Returns whether to skip some XML checks and be fast instead
        """
        ...
    
    def getWriteIndex(self) -> bool:
        """
        Cython signature: bool getWriteIndex()
        Returns whether to write an index at the end of the file (e.g. indexedmzML file format)
        """
        ...
    
    def setWriteIndex(self, write_index: bool ) -> None:
        """
        Cython signature: void setWriteIndex(bool write_index)
        Returns whether to write an index at the end of the file (e.g. indexedmzML file format)
        """
        ...
    
    def getNumpressConfigurationMassTime(self) -> NumpressConfig:
        """
        Cython signature: NumpressConfig getNumpressConfigurationMassTime()
        Sets numpress configuration options for m/z or rt dimension
        """
        ...
    
    def setNumpressConfigurationMassTime(self, config: NumpressConfig ) -> None:
        """
        Cython signature: void setNumpressConfigurationMassTime(NumpressConfig config)
        Returns numpress configuration options for m/z or rt dimension
        """
        ...
    
    def getNumpressConfigurationIntensity(self) -> NumpressConfig:
        """
        Cython signature: NumpressConfig getNumpressConfigurationIntensity()
        Sets numpress configuration options for intensity dimension
        """
        ...
    
    def setNumpressConfigurationIntensity(self, config: NumpressConfig ) -> None:
        """
        Cython signature: void setNumpressConfigurationIntensity(NumpressConfig config)
        Returns numpress configuration options for intensity dimension
        """
        ...
    
    def getNumpressConfigurationFloatDataArray(self) -> NumpressConfig:
        """
        Cython signature: NumpressConfig getNumpressConfigurationFloatDataArray()
        Sets numpress configuration options for float data arrays
        """
        ...
    
    def setNumpressConfigurationFloatDataArray(self, config: NumpressConfig ) -> None:
        """
        Cython signature: void setNumpressConfigurationFloatDataArray(NumpressConfig config)
        Returns numpress configuration options for float data arrays
        """
        ...
    
    def setForceMQCompatability(self, forceMQ: bool ) -> None:
        """
        Cython signature: void setForceMQCompatability(bool forceMQ)
        [mzXML only!]Returns Whether to write a scan-index and meta data to indicate a Thermo FTMS/ITMS instrument (required to have parameter control in MQ)
        """
        ...
    
    def getForceMQCompatability(self) -> bool:
        """
        Cython signature: bool getForceMQCompatability()
        [mzXML only!]Returns Whether to write a scan-index and meta data to indicate a Thermo FTMS/ITMS instrument (required to have parameter control in MQ)
        """
        ...
    
    def setForceTPPCompatability(self, forceTPP: bool ) -> None:
        """
        Cython signature: void setForceTPPCompatability(bool forceTPP)
        [ mzML only!]Returns Whether to skip writing the \<isolationWindow\> tag so that TPP finds the correct precursor m/z
        """
        ...
    
    def getForceTPPCompatability(self) -> bool:
        """
        Cython signature: bool getForceTPPCompatability()
        [mzML only!]Returns Whether to skip writing the \<isolationWindow\> tag so that TPP finds the correct precursor m/z
        """
        ... 


class PeptideEvidence:
    """
    Cython implementation of _PeptideEvidence

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeptideEvidence.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeptideEvidence()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeptideEvidence ) -> None:
        """
        Cython signature: void PeptideEvidence(PeptideEvidence &)
        """
        ...
    
    def setStart(self, start: int ) -> None:
        """
        Cython signature: void setStart(int start)
        Sets the position of the last AA of the peptide in protein coordinates (starting at 0 for the N-terminus). If not available, set to UNKNOWN_POSITION. N-terminal positions must be marked with `N_TERMINAL_AA`
        """
        ...
    
    def getStart(self) -> int:
        """
        Cython signature: int getStart()
        Returns the position in the protein (starting at 0 for the N-terminus). If not available UNKNOWN_POSITION constant is returned
        """
        ...
    
    def setEnd(self, end: int ) -> None:
        """
        Cython signature: void setEnd(int end)
        Sets the position of the last AA of the peptide in protein coordinates (starting at 0 for the N-terminus). If not available, set UNKNOWN_POSITION. C-terminal positions must be marked with C_TERMINAL_AA
        """
        ...
    
    def getEnd(self) -> int:
        """
        Cython signature: int getEnd()
        Returns the position of the last AA of the peptide in protein coordinates (starting at 0 for the N-terminus). If not available UNKNOWN_POSITION constant is returned
        """
        ...
    
    def setAABefore(self, rhs: bytes ) -> None:
        """
        Cython signature: void setAABefore(char rhs)
        Sets the amino acid single letter code before the sequence (preceding amino acid in the protein). If not available, set to UNKNOWN_AA. If N-terminal set to N_TERMINAL_AA
        """
        ...
    
    def getAABefore(self) -> bytes:
        """
        Cython signature: char getAABefore()
        Returns the amino acid single letter code before the sequence (preceding amino acid in the protein). If not available, UNKNOWN_AA is returned. If N-terminal, N_TERMINAL_AA is returned
        """
        ...
    
    def setAAAfter(self, rhs: bytes ) -> None:
        """
        Cython signature: void setAAAfter(char rhs)
        Sets the amino acid single letter code after the sequence (subsequent amino acid in the protein). If not available, set to UNKNOWN_AA. If C-terminal set to C_TERMINAL_AA
        """
        ...
    
    def getAAAfter(self) -> bytes:
        """
        Cython signature: char getAAAfter()
        Returns the amino acid single letter code after the sequence (subsequent amino acid in the protein). If not available, UNKNOWN_AA is returned. If C-terminal, C_TERMINAL_AA is returned
        """
        ...
    
    def setProteinAccession(self, s: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setProteinAccession(String s)
        Sets the protein accession the peptide matches to. If not available set to empty string
        """
        ...
    
    def getProteinAccession(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getProteinAccession()
        Returns the protein accession the peptide matches to. If not available the empty string is returned
        """
        ...
    
    def hasValidLimits(self) -> bool:
        """
        Cython signature: bool hasValidLimits()
        Start and end numbers in evidence represent actual numeric indices
        """
        ...
    
    def __richcmp__(self, other: PeptideEvidence, op: int) -> Any:
        ... 


class PercolatorInfile:
    """
    Cython implementation of _PercolatorInfile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PercolatorInfile.html>`_

    Class for storing Percolator tab-delimited input files
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PercolatorInfile()
        """
        ...
    
    @overload
    def __init__(self, in_0: PercolatorInfile ) -> None:
        """
        Cython signature: void PercolatorInfile(PercolatorInfile &)
        """
        ...
    
    store: __static_PercolatorInfile_store 


class PercolatorOutfile:
    """
    Cython implementation of _PercolatorOutfile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PercolatorOutfile.html>`_

    Class for reading Percolator tab-delimited output files
    
    For PSM-level output, the file extension should be ".psms"
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PercolatorOutfile()
        """
        ...
    
    @overload
    def __init__(self, in_0: PercolatorOutfile ) -> None:
        """
        Cython signature: void PercolatorOutfile(PercolatorOutfile &)
        """
        ...
    
    def getScoreType(self, score_type_name: Union[bytes, str, String] ) -> int:
        """
        Cython signature: PercolatorOutfile_ScoreType getScoreType(String score_type_name)
        Returns a score type given its name
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , proteins: ProteinIdentification , peptides: List[PeptideIdentification] , lookup: SpectrumMetaDataLookup , output_score: int ) -> None:
        """
        Cython signature: void load(const String & filename, ProteinIdentification & proteins, libcpp_vector[PeptideIdentification] & peptides, SpectrumMetaDataLookup & lookup, PercolatorOutfile_ScoreType output_score)
        Loads a Percolator output file
        """
        ...
    PercolatorOutfile_ScoreType : __PercolatorOutfile_ScoreType 


class ProteinProteinCrossLink:
    """
    Cython implementation of _ProteinProteinCrossLink

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::OPXLDataStructs_1_1ProteinProteinCrossLink.html>`_
    """
    
    alpha: AASequence
    
    beta: AASequence
    
    cross_link_position: List[int, int]
    
    cross_linker_mass: float
    
    cross_linker_name: Union[bytes, str, String]
    
    term_spec_alpha: int
    
    term_spec_beta: int
    
    precursor_correction: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProteinProteinCrossLink()
        """
        ...
    
    @overload
    def __init__(self, in_0: ProteinProteinCrossLink ) -> None:
        """
        Cython signature: void ProteinProteinCrossLink(ProteinProteinCrossLink &)
        """
        ...
    
    def getType(self) -> int:
        """
        Cython signature: ProteinProteinCrossLinkType getType()
        """
        ...
    
    def __richcmp__(self, other: ProteinProteinCrossLink, op: int) -> Any:
        ... 


class RNaseDB:
    """
    Cython implementation of _RNaseDB

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1RNaseDB.html>`_
    """
    
    def getEnzyme(self, name: Union[bytes, str, String] ) -> DigestionEnzymeRNA:
        """
        Cython signature: const DigestionEnzymeRNA * getEnzyme(const String & name)
        """
        ...
    
    def getEnzymeByRegEx(self, cleavage_regex: Union[bytes, str, String] ) -> DigestionEnzymeRNA:
        """
        Cython signature: const DigestionEnzymeRNA * getEnzymeByRegEx(const String & cleavage_regex)
        """
        ...
    
    def getAllNames(self, all_names: List[bytes] ) -> None:
        """
        Cython signature: void getAllNames(libcpp_vector[String] & all_names)
        """
        ...
    
    def hasEnzyme(self, name: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasEnzyme(const String & name)
        """
        ... 


class RankScaler:
    """
    Cython implementation of _RankScaler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1RankScaler.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void RankScaler()
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


class RansacModelQuadratic:
    """
    Cython implementation of _RansacModelQuadratic

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1RansacModelQuadratic.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RansacModelQuadratic()
        """
        ...
    
    @overload
    def __init__(self, in_0: RansacModelQuadratic ) -> None:
        """
        Cython signature: void RansacModelQuadratic(RansacModelQuadratic &)
        """
        ... 


class Sample:
    """
    Cython implementation of _Sample

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Sample.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Sample()
        """
        ...
    
    @overload
    def __init__(self, in_0: Sample ) -> None:
        """
        Cython signature: void Sample(Sample &)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        """
        ...
    
    def getOrganism(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOrganism()
        """
        ...
    
    def setOrganism(self, organism: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setOrganism(String organism)
        """
        ...
    
    def getNumber(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNumber()
        Returns the sample number
        """
        ...
    
    def setNumber(self, number: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNumber(String number)
        Sets the sample number (e.g. sample ID)
        """
        ...
    
    def getComment(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getComment()
        Returns the comment (default "")
        """
        ...
    
    def setComment(self, comment: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setComment(String comment)
        Sets the comment (may contain newline characters)
        """
        ...
    
    def getState(self) -> int:
        """
        Cython signature: SampleState getState()
        Returns the state of aggregation (default SAMPLENULL)
        """
        ...
    
    def setState(self, state: int ) -> None:
        """
        Cython signature: void setState(SampleState state)
        Sets the state of aggregation
        """
        ...
    
    def getMass(self) -> float:
        """
        Cython signature: double getMass()
        Returns the mass (in gram) (default 0.0)
        """
        ...
    
    def setMass(self, mass: float ) -> None:
        """
        Cython signature: void setMass(double mass)
        Sets the mass (in gram)
        """
        ...
    
    def getVolume(self) -> float:
        """
        Cython signature: double getVolume()
        Returns the volume (in ml) (default 0.0)
        """
        ...
    
    def setVolume(self, volume: float ) -> None:
        """
        Cython signature: void setVolume(double volume)
        Sets the volume (in ml)
        """
        ...
    
    def getConcentration(self) -> float:
        """
        Cython signature: double getConcentration()
        Returns the concentration (in g/l) (default 0.0)
        """
        ...
    
    def setConcentration(self, concentration: float ) -> None:
        """
        Cython signature: void setConcentration(double concentration)
        Sets the concentration (in g/l)
        """
        ...
    
    def getSubsamples(self) -> List[Sample]:
        """
        Cython signature: libcpp_vector[Sample] getSubsamples()
        Returns a reference to the vector of subsamples that were combined to create this sample
        """
        ...
    
    def setSubsamples(self, subsamples: List[Sample] ) -> None:
        """
        Cython signature: void setSubsamples(libcpp_vector[Sample] subsamples)
        Sets the vector of subsamples that were combined to create this sample
        """
        ...
    
    def removeTreatment(self, position: int ) -> None:
        """
        Cython signature: void removeTreatment(unsigned int position)
        Brief removes the sample treatment at the given position
        """
        ...
    
    def countTreatments(self) -> int:
        """
        Cython signature: int countTreatments()
        Returns the number of sample treatments
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
    
    def __richcmp__(self, other: Sample, op: int) -> Any:
        ...
    SampleState : __SampleState 


class Seed:
    """
    Cython implementation of _Seed

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::FeatureFinderAlgorithmPickedHelperStructs_1_1Seed.html>`_
    """
    
    spectrum: int
    
    peak: int
    
    intensity: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Seed()
        """
        ...
    
    @overload
    def __init__(self, in_0: Seed ) -> None:
        """
        Cython signature: void Seed(Seed &)
        """
        ...
    
    def __richcmp__(self, other: Seed, op: int) -> Any:
        ... 


class SemanticValidator:
    """
    Cython implementation of _SemanticValidator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1SemanticValidator.html>`_
    """
    
    def __init__(self, mapping: CVMappings , cv: ControlledVocabulary ) -> None:
        """
        Cython signature: void SemanticValidator(CVMappings mapping, ControlledVocabulary cv)
        """
        ...
    
    def validate(self, filename: Union[bytes, str, String] , errors: List[bytes] , warnings: List[bytes] ) -> bool:
        """
        Cython signature: bool validate(String filename, StringList errors, StringList warnings)
        """
        ...
    
    def locateTerm(self, path: Union[bytes, str, String] , parsed_term: SemanticValidator_CVTerm ) -> bool:
        """
        Cython signature: bool locateTerm(String path, SemanticValidator_CVTerm & parsed_term)
        Checks if a CVTerm is allowed in a given path
        """
        ...
    
    def setTag(self, tag: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTag(String tag)
        Sets the CV parameter tag name (default 'cvParam')
        """
        ...
    
    def setAccessionAttribute(self, accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setAccessionAttribute(String accession)
        Sets the name of the attribute for accessions in the CV parameter tag name (default 'accession')
        """
        ...
    
    def setNameAttribute(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNameAttribute(String name)
        Sets the name of the attribute for accessions in the CV parameter tag name (default 'name')
        """
        ...
    
    def setValueAttribute(self, value: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setValueAttribute(String value)
        Sets the name of the attribute for accessions in the CV parameter tag name (default 'value')
        """
        ...
    
    def setCheckTermValueTypes(self, check: bool ) -> None:
        """
        Cython signature: void setCheckTermValueTypes(bool check)
        Sets if CV term value types should be check (enabled by default)
        """
        ...
    
    def setCheckUnits(self, check: bool ) -> None:
        """
        Cython signature: void setCheckUnits(bool check)
        Sets if CV term units should be check (disabled by default)
        """
        ...
    
    def setUnitAccessionAttribute(self, accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setUnitAccessionAttribute(String accession)
        Sets the name of the unit accession attribute (default 'unitAccession')
        """
        ...
    
    def setUnitNameAttribute(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setUnitNameAttribute(String name)
        Sets the name of the unit name attribute (default 'unitName')
        """
        ... 


class SemanticValidator_CVTerm:
    """
    Cython implementation of _SemanticValidator_CVTerm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1SemanticValidator_CVTerm.html>`_
    """
    
    accession: Union[bytes, str, String]
    
    name: Union[bytes, str, String]
    
    value: Union[bytes, str, String]
    
    has_value: bool
    
    unit_accession: Union[bytes, str, String]
    
    has_unit_accession: bool
    
    unit_name: Union[bytes, str, String]
    
    has_unit_name: bool
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SemanticValidator_CVTerm()
        """
        ...
    
    @overload
    def __init__(self, in_0: SemanticValidator_CVTerm ) -> None:
        """
        Cython signature: void SemanticValidator_CVTerm(SemanticValidator_CVTerm &)
        """
        ... 


class SpectrumAccessOpenMSCached:
    """
    Cython implementation of _SpectrumAccessOpenMSCached

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumAccessOpenMSCached.html>`_
      -- Inherits from ['ISpectrumAccess']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMSCached()
        """
        ...
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMSCached(String filename)
        An implementation of the Spectrum Access interface using on-disk caching
        
        This class implements the OpenSWATH Spectrum Access interface
        (ISpectrumAccess) using the CachedmzML class which is able to read and
        write a cached mzML file
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessOpenMSCached ) -> None:
        """
        Cython signature: void SpectrumAccessOpenMSCached(SpectrumAccessOpenMSCached &)
        """
        ...
    
    def getSpectrumById(self, id_: int ) -> OSSpectrum:
        """
        Cython signature: shared_ptr[OSSpectrum] getSpectrumById(int id_)
        Returns a pointer to a spectrum at the given string id
        """
        ...
    
    def getSpectraByRT(self, RT: float , deltaRT: float ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] getSpectraByRT(double RT, double deltaRT)
        Returns a vector of ids of spectra that are within RT +/- deltaRT
        """
        ...
    
    def getNrSpectra(self) -> int:
        """
        Cython signature: size_t getNrSpectra()
        Returns the number of spectra available
        """
        ...
    
    def getChromatogramById(self, id_: int ) -> OSChromatogram:
        """
        Cython signature: shared_ptr[OSChromatogram] getChromatogramById(int id_)
        Returns a pointer to a chromatogram at the given id
        """
        ...
    
    def getNrChromatograms(self) -> int:
        """
        Cython signature: size_t getNrChromatograms()
        Returns the number of chromatograms available
        """
        ...
    
    def getChromatogramNativeID(self, id_: int ) -> str:
        """
        Cython signature: libcpp_utf8_output_string getChromatogramNativeID(int id_)
        """
        ... 


class SpectrumAccessQuadMZTransforming:
    """
    Cython implementation of _SpectrumAccessQuadMZTransforming

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumAccessQuadMZTransforming.html>`_
      -- Inherits from ['SpectrumAccessTransforming']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectrumAccessQuadMZTransforming()
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessQuadMZTransforming ) -> None:
        """
        Cython signature: void SpectrumAccessQuadMZTransforming(SpectrumAccessQuadMZTransforming &)
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessOpenMS , a: float , b: float , c: float , ppm: bool ) -> None:
        """
        Cython signature: void SpectrumAccessQuadMZTransforming(shared_ptr[SpectrumAccessOpenMS], double a, double b, double c, bool ppm)
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessOpenMSCached , a: float , b: float , c: float , ppm: bool ) -> None:
        """
        Cython signature: void SpectrumAccessQuadMZTransforming(shared_ptr[SpectrumAccessOpenMSCached], double a, double b, double c, bool ppm)
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessOpenMSInMemory , a: float , b: float , c: float , ppm: bool ) -> None:
        """
        Cython signature: void SpectrumAccessQuadMZTransforming(shared_ptr[SpectrumAccessOpenMSInMemory], double a, double b, double c, bool ppm)
        """
        ...
    
    def getSpectrumById(self, id_: int ) -> OSSpectrum:
        """
        Cython signature: shared_ptr[OSSpectrum] getSpectrumById(int id_)
        Returns a pointer to a spectrum at the given string id
        """
        ...
    
    def getSpectraByRT(self, RT: float , deltaRT: float ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] getSpectraByRT(double RT, double deltaRT)
        Returns a vector of ids of spectra that are within RT +/- deltaRT
        """
        ...
    
    def getNrSpectra(self) -> int:
        """
        Cython signature: size_t getNrSpectra()
        Returns the number of spectra available
        """
        ...
    
    def getChromatogramById(self, id_: int ) -> OSChromatogram:
        """
        Cython signature: shared_ptr[OSChromatogram] getChromatogramById(int id_)
        Returns a pointer to a chromatogram at the given id
        """
        ...
    
    def getNrChromatograms(self) -> int:
        """
        Cython signature: size_t getNrChromatograms()
        Returns the number of chromatograms available
        """
        ...
    
    def getChromatogramNativeID(self, id_: int ) -> str:
        """
        Cython signature: libcpp_utf8_output_string getChromatogramNativeID(int id_)
        """
        ... 


class SpectrumLookup:
    """
    Cython implementation of _SpectrumLookup

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumLookup.html>`_
    """
    
    rt_tolerance: float
    
    def __init__(self) -> None:
        """
        Cython signature: void SpectrumLookup()
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        Check if any spectra were set
        """
        ...
    
    def readSpectra(self, spectra: MSExperiment , scan_regexp: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void readSpectra(MSExperiment spectra, String scan_regexp)
        Read and index spectra for later look-up
        
        :param spectra: Container of spectra
        :param scan_regexp: Regular expression for matching scan numbers in spectrum native IDs (must contain the named group "?<SCAN>". For example, "scan=(?<SCAN>\\d+)").
        """
        ...
    
    def findByRT(self, rt: float ) -> int:
        """
        Cython signature: size_t findByRT(double rt)
        Look up spectrum by retention time (RT)
        
        :param rt: Retention time to look up
        :returns: Index of the spectrum that matched
        """
        ...
    
    def findByNativeID(self, native_id: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t findByNativeID(String native_id)
        Look up spectrum by native ID
        
        :param native_id: Native ID to look up
        :returns: Index of the spectrum that matched
        """
        ...
    
    def findByIndex(self, index: int , count_from_one: bool ) -> int:
        """
        Cython signature: size_t findByIndex(size_t index, bool count_from_one)
        Look up spectrum by index (position in the vector of spectra)
        
        :param index: Index to look up
        :param count_from_one: Do indexes start counting at one (default zero)?
        :returns: Index of the spectrum that matched
        """
        ...
    
    def findByScanNumber(self, scan_number: int ) -> int:
        """
        Cython signature: size_t findByScanNumber(size_t scan_number)
        Look up spectrum by scan number (extracted from the native ID)
        
        :param scan_number: Scan number to look up
        :returns: Index of the spectrum that matched
        """
        ...
    
    def findByReference(self, spectrum_ref: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t findByReference(String spectrum_ref)
        Look up spectrum by reference
        
        :param spectrum_ref: Spectrum reference to parse
        :returns: Index of the spectrum that matched
        """
        ...
    
    def addReferenceFormat(self, regexp: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addReferenceFormat(String regexp)
        Register a possible format for a spectrum reference
        
        :param regexp: Regular expression defining the format
        """
        ...
    
    def extractScanNumber(self, native_id: Union[bytes, str, String] , native_id_type_accession: Union[bytes, str, String] ) -> int:
        """
        Cython signature: int extractScanNumber(const String & native_id, const String & native_id_type_accession)
        """
        ... 


class StringDataArray:
    """
    Cython implementation of _StringDataArray

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::DataArrays_1_1StringDataArray.html>`_
      -- Inherits from ['MetaInfoDescription']

    The representation of extra string data attached to a spectrum or chromatogram.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void StringDataArray()
        """
        ...
    
    @overload
    def __init__(self, in_0: StringDataArray ) -> None:
        """
        Cython signature: void StringDataArray(StringDataArray &)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ...
    
    def resize(self, n: int ) -> None:
        """
        Cython signature: void resize(size_t n)
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ...
    
    def push_back(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void push_back(String)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the peak annotations
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the name of the peak annotations
        """
        ...
    
    def getDataProcessing(self) -> List[DataProcessing]:
        """
        Cython signature: libcpp_vector[shared_ptr[DataProcessing]] getDataProcessing()
        Returns a reference to the description of the applied processing
        """
        ...
    
    def setDataProcessing(self, in_0: List[DataProcessing] ) -> None:
        """
        Cython signature: void setDataProcessing(libcpp_vector[shared_ptr[DataProcessing]])
        Sets the description of the applied processing
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
    
    def __richcmp__(self, other: StringDataArray, op: int) -> Any:
        ... 


class TMTSixteenPlexQuantitationMethod:
    """
    Cython implementation of _TMTSixteenPlexQuantitationMethod

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TMTSixteenPlexQuantitationMethod.html>`_
      -- Inherits from ['IsobaricQuantitationMethod']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TMTSixteenPlexQuantitationMethod()
        """
        ...
    
    @overload
    def __init__(self, in_0: TMTSixteenPlexQuantitationMethod ) -> None:
        """
        Cython signature: void TMTSixteenPlexQuantitationMethod(TMTSixteenPlexQuantitationMethod &)
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


class TheoreticalIsotopePattern:
    """
    Cython implementation of _TheoreticalIsotopePattern

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::FeatureFinderAlgorithmPickedHelperStructs_1_1TheoreticalIsotopePattern.html>`_
    """
    
    intensity: List[float]
    
    optional_begin: int
    
    optional_end: int
    
    max: float
    
    trimmed_left: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TheoreticalIsotopePattern()
        """
        ...
    
    @overload
    def __init__(self, in_0: TheoreticalIsotopePattern ) -> None:
        """
        Cython signature: void TheoreticalIsotopePattern(TheoreticalIsotopePattern &)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        """
        ... 


class TheoreticalSpectrumGenerator:
    """
    Cython implementation of _TheoreticalSpectrumGenerator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TheoreticalSpectrumGenerator.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TheoreticalSpectrumGenerator()
        """
        ...
    
    @overload
    def __init__(self, in_0: TheoreticalSpectrumGenerator ) -> None:
        """
        Cython signature: void TheoreticalSpectrumGenerator(TheoreticalSpectrumGenerator &)
        """
        ...
    
    def getSpectrum(self, spec: MSSpectrum , peptide: AASequence , min_charge: int , max_charge: int ) -> None:
        """
        Cython signature: void getSpectrum(MSSpectrum & spec, AASequence & peptide, int min_charge, int max_charge)
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


class TransitionTSVFile:
    """
    Cython implementation of _TransitionTSVFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TransitionTSVFile.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TransitionTSVFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: TransitionTSVFile ) -> None:
        """
        Cython signature: void TransitionTSVFile(TransitionTSVFile &)
        """
        ...
    
    def convertTargetedExperimentToTSV(self, filename: bytes , targeted_exp: TargetedExperiment ) -> None:
        """
        Cython signature: void convertTargetedExperimentToTSV(char * filename, TargetedExperiment & targeted_exp)
        Write out a targeted experiment (TraML structure) into a tsv file
        """
        ...
    
    @overload
    def convertTSVToTargetedExperiment(self, filename: bytes , filetype: int , targeted_exp: TargetedExperiment ) -> None:
        """
        Cython signature: void convertTSVToTargetedExperiment(char * filename, FileType filetype, TargetedExperiment & targeted_exp)
        Read in a tsv/mrm file and construct a targeted experiment (TraML structure)
        """
        ...
    
    @overload
    def convertTSVToTargetedExperiment(self, filename: bytes , filetype: int , targeted_exp: LightTargetedExperiment ) -> None:
        """
        Cython signature: void convertTSVToTargetedExperiment(char * filename, FileType filetype, LightTargetedExperiment & targeted_exp)
        Read in a tsv file and construct a targeted experiment (Light transition structure)
        """
        ...
    
    def validateTargetedExperiment(self, targeted_exp: TargetedExperiment ) -> None:
        """
        Cython signature: void validateTargetedExperiment(TargetedExperiment targeted_exp)
        Validate a TargetedExperiment (check that all ids are unique)
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


class XLPrecursor:
    """
    Cython implementation of _XLPrecursor

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1XLPrecursor.html>`_
    """
    
    precursor_mass: float
    
    alpha_index: int
    
    beta_index: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void XLPrecursor()
        """
        ...
    
    @overload
    def __init__(self, in_0: XLPrecursor ) -> None:
        """
        Cython signature: void XLPrecursor(XLPrecursor &)
        """
        ... 


class __Averagines:
    None
    C : int
    H : int
    N : int
    O : int
    S : int
    AVERAGINE_NUM : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class DataType:
    None
    STRING_VALUE : int
    INT_VALUE : int
    DOUBLE_VALUE : int
    STRING_LIST : int
    INT_LIST : int
    DOUBLE_LIST : int
    EMPTY_VALUE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __FilterOperation:
    None
    GREATER_EQUAL : int
    EQUAL : int
    LESS_EQUAL : int
    EXISTS : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __FilterType:
    None
    INTENSITY : int
    QUALITY : int
    CHARGE : int
    SIZE : int
    META_DATA : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class IonOpticsType:
    None
    UNKNOWN : int
    MAGNETIC_DEFLECTION : int
    DELAYED_EXTRACTION : int
    COLLISION_QUADRUPOLE : int
    SELECTED_ION_FLOW_TUBE : int
    TIME_LAG_FOCUSING : int
    REFLECTRON : int
    EINZEL_LENS : int
    FIRST_STABILITY_REGION : int
    FRINGING_FIELD : int
    KINETIC_ENERGY_ANALYZER : int
    STATIC_FIELD : int
    SIZE_OF_IONOPTICSTYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class MZTrafoModel_MODELTYPE:
    None
    LINEAR : int
    LINEAR_WEIGHTED : int
    QUADRATIC : int
    QUADRATIC_WEIGHTED : int
    SIZE_OF_MODELTYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __PercolatorOutfile_ScoreType:
    None
    QVALUE : int
    POSTERRPROB : int
    SCORE : int
    SIZE_OF_SCORETYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __ProcessingAction:
    None
    DATA_PROCESSING : int
    CHARGE_DECONVOLUTION : int
    DEISOTOPING : int
    SMOOTHING : int
    CHARGE_CALCULATION : int
    PRECURSOR_RECALCULATION : int
    BASELINE_REDUCTION : int
    PEAK_PICKING : int
    ALIGNMENT : int
    CALIBRATION : int
    NORMALIZATION : int
    FILTERING : int
    QUANTITATION : int
    FEATURE_GROUPING : int
    IDENTIFICATION_MAPPING : int
    FORMAT_CONVERSION : int
    CONVERSION_MZDATA : int
    CONVERSION_MZML : int
    CONVERSION_MZXML : int
    CONVERSION_DTA : int
    IDENTIFICATION : int
    SIZE_OF_PROCESSINGACTION : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __SampleState:
    None
    SAMPLENULL : int
    SOLID : int
    LIQUID : int
    GAS : int
    SOLUTION : int
    EMULSION : int
    SUSPENSION : int
    SIZE_OF_SAMPLESTATE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class UnitType:
    None
    UNIT_ONTOLOGY : int
    MS_ONTOLOGY : int
    OTHER : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class ValueType:
    None
    STRING_VALUE : int
    INT_VALUE : int
    DOUBLE_VALUE : int
    STRING_LIST : int
    INT_LIST : int
    DOUBLE_LIST : int
    EMPTY_VALUE : int

    def getMapping(self) -> Dict[int, str]:
       ... 

