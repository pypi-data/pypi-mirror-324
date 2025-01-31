from __future__ import annotations
from typing import overload, Any, List, Dict, Tuple, Set, Sequence, Union
from pyopenms import *  # pylint: disable=wildcard-import; lgtm(py/polluting-import)
import numpy as _np

from enum import Enum as _PyEnum


def __static_FeatureMapping_assignMS2IndexToFeature(spectra: MSExperiment , fm_info: FeatureMapping_FeatureMappingInfo , precursor_mz_tolerance: float , precursor_rt_tolerance: float , ppm: bool ) -> FeatureMapping_FeatureToMs2Indices:
    """
    Cython signature: FeatureMapping_FeatureToMs2Indices assignMS2IndexToFeature(MSExperiment & spectra, FeatureMapping_FeatureMappingInfo & fm_info, double precursor_mz_tolerance, double precursor_rt_tolerance, bool ppm)
    """
    ...

def __static_AASequence_fromString(s: Union[bytes, str, String] ) -> AASequence:
    """
    Cython signature: AASequence fromString(String s)
        deprecated. Use AASequence(String) instead.
    """
    ...

def __static_NASequence_fromString(s: Union[bytes, str, String] ) -> NASequence:
    """
    Cython signature: NASequence fromString(const String & s)
    """
    ...

def __static_AASequence_fromStringPermissive(s: Union[bytes, str, String] , permissive: bool ) -> AASequence:
    """
    Cython signature: AASequence fromStringPermissive(String s, bool permissive)
        deprecated. Use AASequence(String) instead.
    """
    ...

def __static_TransformationDescription_getModelTypes(result: List[bytes] ) -> None:
    """
    Cython signature: void getModelTypes(StringList result)
    """
    ...


class AASequence:
    """
    Cython implementation of _AASequence

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AASequence.html>`_

    Representation of a peptide/protein sequence
    This class represents amino acid sequences in OpenMS. An AASequence
    instance primarily contains a sequence of residues.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AASequence()
        """
        ...
    
    @overload
    def __init__(self, in_0: AASequence ) -> None:
        """
        Cython signature: void AASequence(AASequence &)
        """
        ...
    
    @overload
    def __init__(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void AASequence(const String &)
        Constructor from amino acid sequence (e.g. "PEPTM(Oxidatio)IDE")
        """
        ...
    
    @overload
    def __init__(self, in_0: Union[bytes, str, String] , permissive: bool ) -> None:
        """
        Cython signature: void AASequence(const String &, bool permissive)
        Constructor from amino acid sequence (e.g. "PEPTM(Oxidatio)IDE"), permissive allows for '+', '*', and '#' in the sequence
        """
        ...
    
    def __add__(self: AASequence, other: AASequence) -> AASequence:
        ...
    
    def __iadd__(self: AASequence, other: AASequence) -> AASequence:
        ...
    
    def __getitem__(self, in_0: int ) -> Residue:
        """
        Cython signature: Residue operator[](size_t)
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        Check if sequence is empty
        """
        ...
    
    def toString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the peptide as string with modifications embedded in brackets
        """
        ...
    
    def toUnmodifiedString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toUnmodifiedString()
        Returns the peptide as string without any modifications
        """
        ...
    
    def toUniModString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toUniModString()
        Returns the peptide as string with UniMod-style modifications embedded in brackets
        """
        ...
    
    @overload
    def toBracketString(self, ) -> Union[bytes, str, String]:
        """
        Cython signature: String toBracketString()
        Create a TPP compatible string of the modified sequence using bracket notation. Uses integer mass by default
        """
        ...
    
    @overload
    def toBracketString(self, integer_mass: bool ) -> Union[bytes, str, String]:
        """
        Cython signature: String toBracketString(bool integer_mass)
        Create a TPP compatible string of the modified sequence using bracket notation
        """
        ...
    
    @overload
    def toBracketString(self, integer_mass: bool , mass_delta: bool ) -> Union[bytes, str, String]:
        """
        Cython signature: String toBracketString(bool integer_mass, bool mass_delta)
        Create a TPP compatible string of the modified sequence using bracket notation.
        """
        ...
    
    @overload
    def toBracketString(self, integer_mass: bool , mass_delta: bool , fixed_modifications: List[bytes] ) -> Union[bytes, str, String]:
        """
        Cython signature: String toBracketString(bool integer_mass, bool mass_delta, libcpp_vector[String] fixed_modifications)
        Create a TPP compatible string of the modified sequence using bracket notation
        """
        ...
    
    @overload
    def setModification(self, index: int , modification: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setModification(size_t index, const String & modification)
        Sets the modification of the residue at position index. If an empty string is passed replaces the residue with its unmodified version
        """
        ...
    
    @overload
    def setModification(self, index: int , modification: ResidueModification ) -> None:
        """
        Cython signature: void setModification(size_t index, const ResidueModification & modification)
        Sets the modification of AA at index by providing a ResidueModification object. Stricter than just looking for the name and adds the Modification to the DB if not present
        """
        ...
    
    def setModificationByDiffMonoMass(self, index: int , diffMonoMass: float ) -> None:
        """
        Cython signature: void setModificationByDiffMonoMass(size_t index, double diffMonoMass)
        Modifies the residue at index in the sequence and potentially in the ResidueDB
        """
        ...
    
    @overload
    def setNTerminalModification(self, modification: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNTerminalModification(String modification)
        Sets the N-terminal modification (by lookup in the mod names of the ModificationsDB). Throws if nothing is found (since the name is not enough information to create a new mod)
        """
        ...
    
    @overload
    def setNTerminalModification(self, mod: ResidueModification ) -> None:
        """
        Cython signature: void setNTerminalModification(const ResidueModification & mod)
        Sets the N-terminal modification (copies and adds to database if not present)
        """
        ...
    
    def setNTerminalModificationByDiffMonoMass(self, diffMonoMass: float , protein_term: bool ) -> None:
        """
        Cython signature: void setNTerminalModificationByDiffMonoMass(double diffMonoMass, bool protein_term)
        Sets the N-terminal modification by the monoisotopic mass difference it introduces (creates a "user-defined" mod if not present)
        """
        ...
    
    @overload
    def setCTerminalModification(self, modification: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCTerminalModification(String modification)
        Sets the C-terminal modification (by lookup in the mod names of the ModificationsDB). Throws if nothing is found (since the name is not enough information to create a new mod)
        """
        ...
    
    @overload
    def setCTerminalModification(self, mod: ResidueModification ) -> None:
        """
        Cython signature: void setCTerminalModification(const ResidueModification & mod)
        Sets the C-terminal modification (copies and adds to database if not present)
        """
        ...
    
    def setCTerminalModificationByDiffMonoMass(self, diffMonoMass: float , protein_term: bool ) -> None:
        """
        Cython signature: void setCTerminalModificationByDiffMonoMass(double diffMonoMass, bool protein_term)
        Sets the C-terminal modification by the monoisotopic mass difference it introduces (creates a "user-defined" mod if not present)
        """
        ...
    
    def getNTerminalModificationName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNTerminalModificationName()
        Returns the name (ID) of the N-terminal modification, or an empty string if none is set
        """
        ...
    
    def getNTerminalModification(self) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getNTerminalModification()
        Returns a copy of the name N-terminal modification object, or None
        """
        ...
    
    def getCTerminalModificationName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCTerminalModificationName()
        Returns the name (ID) of the C-terminal modification, or an empty string if none is set
        """
        ...
    
    def getCTerminalModification(self) -> ResidueModification:
        """
        Cython signature: const ResidueModification * getCTerminalModification()
        Returns a copy of the name C-terminal modification object, or None
        """
        ...
    
    def getResidue(self, index: int ) -> Residue:
        """
        Cython signature: Residue getResidue(size_t index)
        Returns the residue at position index
        """
        ...
    
    @overload
    def getFormula(self, ) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getFormula()
        Convenience function with ResidueType=Full and charge = 0 by default
        """
        ...
    
    @overload
    def getFormula(self, type_: int , charge: int ) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getFormula(ResidueType type_, int charge)
        """
        ...
    
    @overload
    def getAverageWeight(self, ) -> float:
        """
        Cython signature: double getAverageWeight()
        Returns the average weight of the peptide
        """
        ...
    
    @overload
    def getAverageWeight(self, type_: int , charge: int ) -> float:
        """
        Cython signature: double getAverageWeight(ResidueType type_, int charge)
        """
        ...
    
    @overload
    def getMonoWeight(self, ) -> float:
        """
        Cython signature: double getMonoWeight()
        Returns the mono isotopic weight of the peptide
        """
        ...
    
    @overload
    def getMonoWeight(self, type_: int , charge: int ) -> float:
        """
        Cython signature: double getMonoWeight(ResidueType type_, int charge)
        """
        ...
    
    @overload
    def getMZ(self, charge: int ) -> float:
        """
        Cython signature: double getMZ(int charge)
        Returns the mass-to-charge ratio of the peptide
        """
        ...
    
    @overload
    def getMZ(self, charge: int , type_: int ) -> float:
        """
        Cython signature: double getMZ(int charge, ResidueType type_)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        Returns the number of residues
        """
        ...
    
    def getPrefix(self, index: int ) -> AASequence:
        """
        Cython signature: AASequence getPrefix(size_t index)
        Returns a peptide sequence of the first index residues
        """
        ...
    
    def getSuffix(self, index: int ) -> AASequence:
        """
        Cython signature: AASequence getSuffix(size_t index)
        Returns a peptide sequence of the last index residues
        """
        ...
    
    def getSubsequence(self, index: int , number: int ) -> AASequence:
        """
        Cython signature: AASequence getSubsequence(size_t index, unsigned int number)
        Returns a peptide sequence of number residues, beginning at position index
        """
        ...
    
    def has(self, residue: Residue ) -> bool:
        """
        Cython signature: bool has(Residue residue)
        Returns true if the peptide contains the given residue
        """
        ...
    
    def hasSubsequence(self, peptide: AASequence ) -> bool:
        """
        Cython signature: bool hasSubsequence(AASequence peptide)
        Returns true if the peptide contains the given peptide
        """
        ...
    
    def hasPrefix(self, peptide: AASequence ) -> bool:
        """
        Cython signature: bool hasPrefix(AASequence peptide)
        Returns true if the peptide has the given prefix
        """
        ...
    
    def hasSuffix(self, peptide: AASequence ) -> bool:
        """
        Cython signature: bool hasSuffix(AASequence peptide)
        Returns true if the peptide has the given suffix
        """
        ...
    
    def hasNTerminalModification(self) -> bool:
        """
        Cython signature: bool hasNTerminalModification()
        Predicate which is true if the peptide is N-term modified
        """
        ...
    
    def hasCTerminalModification(self) -> bool:
        """
        Cython signature: bool hasCTerminalModification()
        Predicate which is true if the peptide is C-term modified
        """
        ...
    
    def isModified(self) -> bool:
        """
        Cython signature: bool isModified()
        Returns true if any of the residues or termini are modified
        """
        ...
    
    def __str__(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the peptide as string with modifications embedded in brackets
        """
        ...
    
    def __richcmp__(self, other: AASequence, op: int) -> Any:
        ...
    
    fromString: __static_AASequence_fromString
    
    fromStringPermissive: __static_AASequence_fromStringPermissive 


class AScore:
    """
    Cython implementation of _AScore

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AScore.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AScore()
        """
        ...
    
    @overload
    def __init__(self, in_0: AScore ) -> None:
        """
        Cython signature: void AScore(AScore &)
        """
        ...
    
    def compute(self, hit: PeptideHit , real_spectrum: MSSpectrum ) -> PeptideHit:
        """
        Cython signature: PeptideHit compute(PeptideHit & hit, MSSpectrum & real_spectrum)
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


class AbsoluteQuantitation:
    """
    Cython implementation of _AbsoluteQuantitation

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AbsoluteQuantitation.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AbsoluteQuantitation()
        """
        ...
    
    @overload
    def __init__(self, in_0: AbsoluteQuantitation ) -> None:
        """
        Cython signature: void AbsoluteQuantitation(AbsoluteQuantitation &)
        """
        ...
    
    def setQuantMethods(self, quant_methods: List[AbsoluteQuantitationMethod] ) -> None:
        """
        Cython signature: void setQuantMethods(libcpp_vector[AbsoluteQuantitationMethod] & quant_methods)
        """
        ...
    
    def getQuantMethods(self) -> List[AbsoluteQuantitationMethod]:
        """
        Cython signature: libcpp_vector[AbsoluteQuantitationMethod] getQuantMethods()
        """
        ...
    
    def calculateRatio(self, component_1: Feature , component_2: Feature , feature_name: Union[bytes, str, String] ) -> float:
        """
        Cython signature: double calculateRatio(Feature & component_1, Feature & component_2, const String & feature_name)
        """
        ...
    
    def applyCalibration(self, component: Feature , IS_component: Feature , feature_name: Union[bytes, str, String] , transformation_model: Union[bytes, str, String] , transformation_model_params: Param ) -> float:
        """
        Cython signature: double applyCalibration(const Feature & component, const Feature & IS_component, const String & feature_name, const String & transformation_model, const Param & transformation_model_params)
        """
        ...
    
    def quantifyComponents(self, unknowns: FeatureMap ) -> None:
        """
        Cython signature: void quantifyComponents(FeatureMap & unknowns)
        This function applies the calibration curve, hence quantifying all the components
        """
        ...
    
    def optimizeCalibrationCurveIterative(self, component_concentrations: List[AQS_featureConcentration] , feature_name: Union[bytes, str, String] , transformation_model: Union[bytes, str, String] , transformation_model_params: Param , optimized_params: Param ) -> bool:
        """
        Cython signature: bool optimizeCalibrationCurveIterative(libcpp_vector[AQS_featureConcentration] & component_concentrations, const String & feature_name, const String & transformation_model, const Param & transformation_model_params, Param & optimized_params)
        """
        ...
    
    def optimizeSingleCalibrationCurve(self, component_name: Union[bytes, str, String] , component_concentrations: List[AQS_featureConcentration] ) -> None:
        """
        Cython signature: void optimizeSingleCalibrationCurve(const String & component_name, libcpp_vector[AQS_featureConcentration] & component_concentrations)
        """
        ...
    
    def calculateBias(self, actual_concentration: float , calculated_concentration: float ) -> float:
        """
        Cython signature: double calculateBias(double actual_concentration, double calculated_concentration)
        This function calculates the bias of the calibration
        """
        ...
    
    def fitCalibration(self, component_concentrations: List[AQS_featureConcentration] , feature_name: Union[bytes, str, String] , transformation_model: Union[bytes, str, String] , transformation_model_params: Param ) -> Param:
        """
        Cython signature: Param fitCalibration(libcpp_vector[AQS_featureConcentration] & component_concentrations, const String & feature_name, const String & transformation_model, Param transformation_model_params)
        """
        ...
    
    def calculateBiasAndR(self, component_concentrations: List[AQS_featureConcentration] , feature_name: Union[bytes, str, String] , transformation_model: Union[bytes, str, String] , transformation_model_params: Param , biases: List[float] , correlation_coefficient: float ) -> None:
        """
        Cython signature: void calculateBiasAndR(libcpp_vector[AQS_featureConcentration] & component_concentrations, const String & feature_name, const String & transformation_model, Param & transformation_model_params, libcpp_vector[double] & biases, double & correlation_coefficient)
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


class Acquisition:
    """
    Cython implementation of _Acquisition

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Acquisition.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Acquisition()
        """
        ...
    
    @overload
    def __init__(self, in_0: Acquisition ) -> None:
        """
        Cython signature: void Acquisition(Acquisition &)
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        """
        ...
    
    def setIdentifier(self, identifier: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(const String & identifier)
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
    
    def __richcmp__(self, other: Acquisition, op: int) -> Any:
        ... 


class Adduct:
    """
    Cython implementation of _Adduct

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Adduct.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Adduct()
        """
        ...
    
    @overload
    def __init__(self, in_0: Adduct ) -> None:
        """
        Cython signature: void Adduct(Adduct &)
        """
        ...
    
    @overload
    def __init__(self, charge: int ) -> None:
        """
        Cython signature: void Adduct(int charge)
        """
        ...
    
    @overload
    def __init__(self, charge: int , amount: int , singleMass: float , formula: Union[bytes, str, String] , log_prob: float , rt_shift: float , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void Adduct(int charge, int amount, double singleMass, String formula, double log_prob, double rt_shift, String label)
        """
        ...
    
    def getCharge(self) -> int:
        """
        Cython signature: int getCharge()
        """
        ...
    
    def setCharge(self, charge: int ) -> None:
        """
        Cython signature: void setCharge(int charge)
        """
        ...
    
    def getAmount(self) -> int:
        """
        Cython signature: int getAmount()
        """
        ...
    
    def setAmount(self, amount: int ) -> None:
        """
        Cython signature: void setAmount(int amount)
        """
        ...
    
    def getSingleMass(self) -> float:
        """
        Cython signature: double getSingleMass()
        """
        ...
    
    def setSingleMass(self, singleMass: float ) -> None:
        """
        Cython signature: void setSingleMass(double singleMass)
        """
        ...
    
    def getLogProb(self) -> float:
        """
        Cython signature: double getLogProb()
        """
        ...
    
    def setLogProb(self, log_prob: float ) -> None:
        """
        Cython signature: void setLogProb(double log_prob)
        """
        ...
    
    def getFormula(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFormula()
        """
        ...
    
    def setFormula(self, formula: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFormula(String formula)
        """
        ...
    
    def getRTShift(self) -> float:
        """
        Cython signature: double getRTShift()
        """
        ...
    
    def getLabel(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getLabel()
        """
        ... 


class Attachment:
    """
    Cython implementation of _Attachment

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::QcMLFile_1_1Attachment.html>`_
    """
    
    name: Union[bytes, str, String]
    
    id: Union[bytes, str, String]
    
    value: Union[bytes, str, String]
    
    cvRef: Union[bytes, str, String]
    
    cvAcc: Union[bytes, str, String]
    
    unitRef: Union[bytes, str, String]
    
    unitAcc: Union[bytes, str, String]
    
    binary: Union[bytes, str, String]
    
    qualityRef: Union[bytes, str, String]
    
    colTypes: List[bytes]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Attachment()
        """
        ...
    
    @overload
    def __init__(self, in_0: Attachment ) -> None:
        """
        Cython signature: void Attachment(Attachment &)
        """
        ...
    
    def toXMLString(self, indentation_level: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String toXMLString(unsigned int indentation_level)
        """
        ...
    
    def toCSVString(self, separator: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String toCSVString(String separator)
        """
        ...
    
    def __richcmp__(self, other: Attachment, op: int) -> Any:
        ... 


class CVMappings:
    """
    Cython implementation of _CVMappings

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVMappings.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVMappings()
        """
        ...
    
    @overload
    def __init__(self, in_0: CVMappings ) -> None:
        """
        Cython signature: void CVMappings(CVMappings &)
        """
        ...
    
    def setMappingRules(self, cv_mapping_rules: List[CVMappingRule] ) -> None:
        """
        Cython signature: void setMappingRules(libcpp_vector[CVMappingRule] & cv_mapping_rules)
        Sets the mapping rules of the mapping file
        """
        ...
    
    def getMappingRules(self) -> List[CVMappingRule]:
        """
        Cython signature: libcpp_vector[CVMappingRule] getMappingRules()
        Returns the mapping rules
        """
        ...
    
    def addMappingRule(self, cv_mapping_rule: CVMappingRule ) -> None:
        """
        Cython signature: void addMappingRule(CVMappingRule & cv_mapping_rule)
        Adds a mapping rule
        """
        ...
    
    def setCVReferences(self, cv_references: List[CVReference] ) -> None:
        """
        Cython signature: void setCVReferences(libcpp_vector[CVReference] & cv_references)
        Sets the CV references
        """
        ...
    
    def getCVReferences(self) -> List[CVReference]:
        """
        Cython signature: libcpp_vector[CVReference] getCVReferences()
        Returns the CV references
        """
        ...
    
    def addCVReference(self, cv_reference: CVReference ) -> None:
        """
        Cython signature: void addCVReference(CVReference & cv_reference)
        Adds a CV reference
        """
        ...
    
    def hasCVReference(self, identifier: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasCVReference(const String & identifier)
        Returns true if a CV reference is given
        """
        ... 


class CachedMzMLHandler:
    """
    Cython implementation of _CachedMzMLHandler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1CachedMzMLHandler.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CachedMzMLHandler()
        An internal class that handles single spectra and chromatograms
        """
        ...
    
    @overload
    def __init__(self, in_0: CachedMzMLHandler ) -> None:
        """
        Cython signature: void CachedMzMLHandler(CachedMzMLHandler &)
        """
        ...
    
    def writeMemdump(self, exp: MSExperiment , out: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void writeMemdump(MSExperiment exp, String out)
        Write complete spectra as a dump to the disk
        """
        ...
    
    def writeMetadata(self, exp: MSExperiment , out_meta: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void writeMetadata(MSExperiment exp, String out_meta)
        Write only the meta data of an MSExperiment
        """
        ...
    
    def readMemdump(self, exp: MSExperiment , filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void readMemdump(MSExperiment exp, String filename)
        Read all spectra from a dump from the disk
        """
        ...
    
    def getSpectraIndex(self) -> List[streampos]:
        """
        Cython signature: libcpp_vector[streampos] getSpectraIndex()
        """
        ...
    
    def getChromatogramIndex(self) -> List[streampos]:
        """
        Cython signature: libcpp_vector[streampos] getChromatogramIndex()
        """
        ...
    
    def createMemdumpIndex(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void createMemdumpIndex(String filename)
        Create an index on the location of all the spectra and chromatograms
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


class ChromatogramExtractorAlgorithm:
    """
    Cython implementation of _ChromatogramExtractorAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ChromatogramExtractorAlgorithm.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ChromatogramExtractorAlgorithm()
        """
        ...
    
    @overload
    def __init__(self, in_0: ChromatogramExtractorAlgorithm ) -> None:
        """
        Cython signature: void ChromatogramExtractorAlgorithm(ChromatogramExtractorAlgorithm &)
        """
        ...
    
    def extractChromatograms(self, input: SpectrumAccessOpenMS , output: List[OSChromatogram] , extraction_coordinates: List[ExtractionCoordinates] , mz_extraction_window: float , ppm: bool , im_extraction_window: float , filter: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void extractChromatograms(shared_ptr[SpectrumAccessOpenMS] input, libcpp_vector[shared_ptr[OSChromatogram]] & output, libcpp_vector[ExtractionCoordinates] extraction_coordinates, double mz_extraction_window, bool ppm, double im_extraction_window, String filter)
          Extract chromatograms at the m/z and RT defined by the ExtractionCoordinates
        
        
        :param input: Input spectral map
        :param output: Output chromatograms (XICs)
        :param extraction_coordinates: Extracts around these coordinates (from
         rt_start to rt_end in seconds - extracts the whole chromatogram if
         rt_end - rt_start < 0).
        :param mz_extraction_window: Extracts a window of this size in m/z
          dimension in Th or ppm (e.g. a window of 50 ppm means an extraction of
          25 ppm on either side)
        :param ppm: Whether mz_extraction_window is in ppm or in Th
        :param filter: Which function to apply in m/z space (currently "tophat" only)
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


class ChromeleonFile:
    """
    Cython implementation of _ChromeleonFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ChromeleonFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ChromeleonFile()
        Load Chromeleon HPLC text file and save it into a `MSExperiment`.
        """
        ...
    
    @overload
    def __init__(self, in_0: ChromeleonFile ) -> None:
        """
        Cython signature: void ChromeleonFile(ChromeleonFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , experiment: MSExperiment ) -> None:
        """
        Cython signature: void load(const String & filename, MSExperiment & experiment)
        Load the file's data and metadata, and save it into a `MSExperiment`
        """
        ... 


class ColumnHeader:
    """
    Cython implementation of _ColumnHeader

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ConsensusMap_1_1ColumnHeader.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    filename: Union[bytes, str, String]
    
    label: Union[bytes, str, String]
    
    size: int
    
    unique_id: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ColumnHeader()
        """
        ...
    
    @overload
    def __init__(self, in_0: ColumnHeader ) -> None:
        """
        Cython signature: void ColumnHeader(ColumnHeader &)
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
    
    def __richcmp__(self, other: ColumnHeader, op: int) -> Any:
        ... 


class ConsensusIDAlgorithmAverage:
    """
    Cython implementation of _ConsensusIDAlgorithmAverage

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusIDAlgorithmAverage.html>`_
      -- Inherits from ['ConsensusIDAlgorithmIdentity']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusIDAlgorithmAverage()
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


class ConsensusIDAlgorithmPEPMatrix:
    """
    Cython implementation of _ConsensusIDAlgorithmPEPMatrix

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusIDAlgorithmPEPMatrix.html>`_
      -- Inherits from ['ConsensusIDAlgorithmSimilarity']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusIDAlgorithmPEPMatrix()
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


class ConsensusIDAlgorithmRanks:
    """
    Cython implementation of _ConsensusIDAlgorithmRanks

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusIDAlgorithmRanks.html>`_
      -- Inherits from ['ConsensusIDAlgorithmIdentity']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusIDAlgorithmRanks()
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


class ConsensusMap:
    """
    Cython implementation of _ConsensusMap

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::ConsensusMap_1_1ConsensusMap.html>`_
      -- Inherits from ['UniqueIdInterface', 'DocumentIdentifier', 'RangeManagerRtMzInt', 'MetaInfoInterface']

    A container for consensus elements.
    
    A ConsensusMap is a container holding 2-dimensional consensus elements
    (ConsensusFeature) which in turn represent analytes that have been
    quantified across multiple LC-MS/MS experiments. Each analyte in a
    ConsensusFeature is linked to its original LC-MS/MS run, the links are
    maintained by the ConsensusMap class.
    The map is implemented as a vector of elements of type ConsensusFeature.
    
    To be consistent, all maps who are referenced by ConsensusFeature objects
    (through a unique id) need to be registered in this class.
    
    This class supports direct iteration in Python.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ConsensusMap()
        """
        ...
    
    @overload
    def __init__(self, in_0: ConsensusMap ) -> None:
        """
        Cython signature: void ConsensusMap(ConsensusMap &)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: int size()
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
    
    def __getitem__(self, in_0: int ) -> ConsensusFeature:
        """
        Cython signature: ConsensusFeature & operator[](size_t)
        """
        ...
    def __setitem__(self, key: int, value: ConsensusFeature ) -> None:
        """Cython signature: ConsensusFeature & operator[](size_t)"""
        ...
    
    def push_back(self, spec: ConsensusFeature ) -> None:
        """
        Cython signature: void push_back(ConsensusFeature spec)
        """
        ...
    
    def appendRows(self, in_0: ConsensusMap ) -> ConsensusMap:
        """
        Cython signature: ConsensusMap appendRows(ConsensusMap)
        Add consensus map entries as new rows
        """
        ...
    
    def appendColumns(self, in_0: ConsensusMap ) -> ConsensusMap:
        """
        Cython signature: ConsensusMap appendColumns(ConsensusMap)
        Add consensus map entries as new columns
        """
        ...
    
    @overload
    def clear(self, clear_meta_data: bool ) -> None:
        """
        Cython signature: void clear(bool clear_meta_data)
        Clears all data and meta data
        """
        ...
    
    @overload
    def clear(self, ) -> None:
        """
        Cython signature: void clear()
        """
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
        Returns a const reference to the description of the applied data processing
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
        Sets the file paths to the primary MS run (stored in ColumnHeaders)
        """
        ...
    
    @overload
    def setPrimaryMSRunPath(self, s: List[bytes] , e: MSExperiment ) -> None:
        """
        Cython signature: void setPrimaryMSRunPath(StringList & s, MSExperiment & e)
        """
        ...
    
    def getPrimaryMSRunPath(self, toFill: List[bytes] ) -> None:
        """
        Cython signature: void getPrimaryMSRunPath(StringList & toFill)
        Returns the MS run path (stored in ColumnHeaders)
        """
        ...
    
    @overload
    def sortByIntensity(self, reverse: bool ) -> None:
        """
        Cython signature: void sortByIntensity(bool reverse)
        Sorts the peaks according to ascending intensity.
        """
        ...
    
    @overload
    def sortByIntensity(self, ) -> None:
        """
        Cython signature: void sortByIntensity()
        """
        ...
    
    def sortByRT(self) -> None:
        """
        Cython signature: void sortByRT()
        Sorts the peaks according to RT position
        """
        ...
    
    def sortByMZ(self) -> None:
        """
        Cython signature: void sortByMZ()
        Sorts the peaks according to m/z position
        """
        ...
    
    def sortByPosition(self) -> None:
        """
        Cython signature: void sortByPosition()
        Lexicographically sorts the peaks by their position (First RT then m/z)
        """
        ...
    
    @overload
    def sortByQuality(self, reverse: bool ) -> None:
        """
        Cython signature: void sortByQuality(bool reverse)
        Sorts the peaks according to ascending quality.
        """
        ...
    
    @overload
    def sortByQuality(self, ) -> None:
        """
        Cython signature: void sortByQuality()
        """
        ...
    
    def sortBySize(self) -> None:
        """
        Cython signature: void sortBySize()
        Sorts with respect to the size (number of elements)
        """
        ...
    
    def sortByMaps(self) -> None:
        """
        Cython signature: void sortByMaps()
        Sorts with respect to the sets of maps covered by the consensus features (lexicographically)
        """
        ...
    
    def getExperimentType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getExperimentType()
        Non-mutable access to the experiment type
        """
        ...
    
    def setExperimentType(self, experiment_type: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setExperimentType(String experiment_type)
        Mutable access to the experiment type
        """
        ...
    
    def sortPeptideIdentificationsByMapIndex(self) -> None:
        """
        Cython signature: void sortPeptideIdentificationsByMapIndex()
        Sorts PeptideIdentifications of consensus features with respect to their map index.
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
    
    def __richcmp__(self, other: ConsensusMap, op: int) -> Any:
        ...
    
    def __iter__(self) -> ConsensusFeature:
       ... 


class CubicSpline2d:
    """
    Cython implementation of _CubicSpline2d

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CubicSpline2d.html>`_
    """
    
    @overload
    def __init__(self, x: List[float] , y: List[float] ) -> None:
        """
        Cython signature: void CubicSpline2d(libcpp_vector[double] x, libcpp_vector[double] y)
        """
        ...
    
    @overload
    def __init__(self, in_0: CubicSpline2d ) -> None:
        """
        Cython signature: void CubicSpline2d(CubicSpline2d &)
        """
        ...
    
    @overload
    def __init__(self, m: Dict[float, float] ) -> None:
        """
        Cython signature: void CubicSpline2d(libcpp_map[double,double] m)
        """
        ...
    
    def eval(self, x: float ) -> float:
        """
        Cython signature: double eval(double x)
        Evaluates the cubic spline
        """
        ...
    
    def derivatives(self, x: float , order: int ) -> float:
        """
        Cython signature: double derivatives(double x, unsigned int order)
        Returns first, second or third derivative of cubic spline
        """
        ... 


class DRange1:
    """
    Cython implementation of _DRange1

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DRange1.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DRange1()
        """
        ...
    
    @overload
    def __init__(self, in_0: DRange1 ) -> None:
        """
        Cython signature: void DRange1(DRange1 &)
        """
        ...
    
    @overload
    def __init__(self, lower: DPosition1 , upper: DPosition1 ) -> None:
        """
        Cython signature: void DRange1(DPosition1 lower, DPosition1 upper)
        """
        ...
    
    def encloses(self, position: DPosition1 ) -> bool:
        """
        Cython signature: bool encloses(DPosition1 & position)
        """
        ...
    
    def united(self, other_range: DRange1 ) -> DRange1:
        """
        Cython signature: DRange1 united(DRange1 other_range)
        """
        ...
    
    def isIntersected(self, range_: DRange1 ) -> bool:
        """
        Cython signature: bool isIntersected(DRange1 & range_)
        """
        ...
    
    def isEmpty(self) -> bool:
        """
        Cython signature: bool isEmpty()
        """
        ...
    
    def __richcmp__(self, other: DRange1, op: int) -> Any:
        ... 


class DRange2:
    """
    Cython implementation of _DRange2

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DRange2.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DRange2()
        """
        ...
    
    @overload
    def __init__(self, in_0: DRange2 ) -> None:
        """
        Cython signature: void DRange2(DRange2 &)
        """
        ...
    
    @overload
    def __init__(self, lower: Union[Sequence[int], Sequence[float]] , upper: Union[Sequence[int], Sequence[float]] ) -> None:
        """
        Cython signature: void DRange2(DPosition2 lower, DPosition2 upper)
        """
        ...
    
    @overload
    def __init__(self, minx: float , miny: float , maxx: float , maxy: float ) -> None:
        """
        Cython signature: void DRange2(double minx, double miny, double maxx, double maxy)
        """
        ...
    
    def united(self, other_range: DRange2 ) -> DRange2:
        """
        Cython signature: DRange2 united(DRange2 other_range)
        """
        ...
    
    def isIntersected(self, range_: DRange2 ) -> bool:
        """
        Cython signature: bool isIntersected(DRange2 & range_)
        """
        ...
    
    def isEmpty(self) -> bool:
        """
        Cython signature: bool isEmpty()
        """
        ...
    
    def __richcmp__(self, other: DRange2, op: int) -> Any:
        ... 


class DTAFile:
    """
    Cython implementation of _DTAFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DTAFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DTAFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: DTAFile ) -> None:
        """
        Cython signature: void DTAFile(DTAFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void load(String filename, MSSpectrum & spectrum)
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void store(String filename, MSSpectrum & spectrum)
        """
        ... 


class Date:
    """
    Cython implementation of _Date

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Date.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Date()
        """
        ...
    
    @overload
    def __init__(self, in_0: Date ) -> None:
        """
        Cython signature: void Date(Date &)
        """
        ...
    
    def set(self, date: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void set(const String & date)
        """
        ...
    
    def today(self) -> Date:
        """
        Cython signature: Date today()
        """
        ...
    
    def get(self) -> Union[bytes, str, String]:
        """
        Cython signature: String get()
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ... 


class Digestion:
    """
    Cython implementation of _Digestion

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Digestion.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Digestion()
        """
        ...
    
    @overload
    def __init__(self, in_0: Digestion ) -> None:
        """
        Cython signature: void Digestion(Digestion &)
        """
        ...
    
    def getEnzyme(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getEnzyme()
        Returns the enzyme name (default is "")
        """
        ...
    
    def setEnzyme(self, enzyme: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setEnzyme(const String & enzyme)
        Sets the enzyme name
        """
        ...
    
    def getDigestionTime(self) -> float:
        """
        Cython signature: double getDigestionTime()
        Returns the digestion time in minutes (default is 0.0)
        """
        ...
    
    def setDigestionTime(self, digestion_time: float ) -> None:
        """
        Cython signature: void setDigestionTime(double digestion_time)
        Sets the digestion time in minutes
        """
        ...
    
    def getTemperature(self) -> float:
        """
        Cython signature: double getTemperature()
        Returns the temperature during digestion in degree C (default is 0.0)
        """
        ...
    
    def setTemperature(self, temperature: float ) -> None:
        """
        Cython signature: void setTemperature(double temperature)
        Sets the temperature during digestion in degree C
        """
        ...
    
    def getPh(self) -> float:
        """
        Cython signature: double getPh()
        Returns the pH value (default is 0.0)
        """
        ...
    
    def setPh(self, ph: float ) -> None:
        """
        Cython signature: void setPh(double ph)
        Sets the pH value
        """
        ... 


class ExtractionCoordinates:
    """
    Cython implementation of _ExtractionCoordinates

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ExtractionCoordinates.html>`_
    """
    
    mz: float
    
    mz_precursor: float
    
    rt_start: float
    
    rt_end: float
    
    ion_mobility: float
    
    id: bytes
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ExtractionCoordinates()
        """
        ...
    
    @overload
    def __init__(self, in_0: ExtractionCoordinates ) -> None:
        """
        Cython signature: void ExtractionCoordinates(ExtractionCoordinates)
        """
        ... 


class FeatureDeconvolution:
    """
    Cython implementation of _FeatureDeconvolution

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureDeconvolution.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureDeconvolution()
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureDeconvolution ) -> None:
        """
        Cython signature: void FeatureDeconvolution(FeatureDeconvolution &)
        """
        ...
    
    def compute(self, input: FeatureMap , output: FeatureMap , cmap1: ConsensusMap , cmap2: ConsensusMap ) -> None:
        """
        Cython signature: void compute(FeatureMap & input, FeatureMap & output, ConsensusMap & cmap1, ConsensusMap & cmap2)
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
    CHARGEMODE_FD : __CHARGEMODE_FD 


class FeatureFindingMetabo:
    """
    Cython implementation of _FeatureFindingMetabo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureFindingMetabo.html>`_
      -- Inherits from ['ProgressLogger', 'DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureFindingMetabo()
        Method for the assembly of mass traces belonging to the same isotope
        pattern, i.e., that are compatible in retention times, mass-to-charge ratios,
        and isotope abundances
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureFindingMetabo ) -> None:
        """
        Cython signature: void FeatureFindingMetabo(FeatureFindingMetabo &)
        """
        ...
    
    def run(self, input_mtraces: List[Kernel_MassTrace] , output_featmap: FeatureMap , output_chromatograms: List[List[MSChromatogram]] ) -> None:
        """
        Cython signature: void run(libcpp_vector[Kernel_MassTrace] input_mtraces, FeatureMap & output_featmap, libcpp_vector[libcpp_vector[MSChromatogram]] & output_chromatograms)
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


class FeatureGroupingAlgorithmQT:
    """
    Cython implementation of _FeatureGroupingAlgorithmQT

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureGroupingAlgorithmQT.html>`_
      -- Inherits from ['FeatureGroupingAlgorithm']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureGroupingAlgorithmQT()
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


class FeatureMapping:
    """
    Cython implementation of _FeatureMapping

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureMapping.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureMapping()
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureMapping ) -> None:
        """
        Cython signature: void FeatureMapping(FeatureMapping &)
        """
        ...
    
    assignMS2IndexToFeature: __static_FeatureMapping_assignMS2IndexToFeature 


class FeatureMapping_FeatureMappingInfo:
    """
    Cython implementation of _FeatureMapping_FeatureMappingInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureMapping_FeatureMappingInfo.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureMapping_FeatureMappingInfo()
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureMapping_FeatureMappingInfo ) -> None:
        """
        Cython signature: void FeatureMapping_FeatureMappingInfo(FeatureMapping_FeatureMappingInfo &)
        """
        ... 


class FeatureMapping_FeatureToMs2Indices:
    """
    Cython implementation of _FeatureMapping_FeatureToMs2Indices

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureMapping_FeatureToMs2Indices.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureMapping_FeatureToMs2Indices()
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureMapping_FeatureToMs2Indices ) -> None:
        """
        Cython signature: void FeatureMapping_FeatureToMs2Indices(FeatureMapping_FeatureToMs2Indices &)
        """
        ... 


class FloatDataArray:
    """
    Cython implementation of _FloatDataArray

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::DataArrays_1_1FloatDataArray.html>`_
      -- Inherits from ['MetaInfoDescription']

    The representation of extra float data attached to a spectrum or chromatogram.
    Raw data access is proved by `get_peaks` and `set_peaks`, which yields numpy arrays
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FloatDataArray()
        """
        ...
    
    @overload
    def __init__(self, in_0: FloatDataArray ) -> None:
        """
        Cython signature: void FloatDataArray(FloatDataArray &)
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
    
    def reserve(self, n: int ) -> None:
        """
        Cython signature: void reserve(size_t n)
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ...
    
    def push_back(self, in_0: float ) -> None:
        """
        Cython signature: void push_back(float)
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
    
    def __richcmp__(self, other: FloatDataArray, op: int) -> Any:
        ... 


class InstrumentSettings:
    """
    Cython implementation of _InstrumentSettings

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1InstrumentSettings.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void InstrumentSettings()
        Description of the settings a MS Instrument was run with
        """
        ...
    
    @overload
    def __init__(self, in_0: InstrumentSettings ) -> None:
        """
        Cython signature: void InstrumentSettings(InstrumentSettings &)
        """
        ...
    
    def getPolarity(self) -> int:
        """
        Cython signature: Polarity getPolarity()
        Returns the polarity
        """
        ...
    
    def setPolarity(self, in_0: int ) -> None:
        """
        Cython signature: void setPolarity(Polarity)
        Sets the polarity
        """
        ...
    
    def getScanMode(self) -> int:
        """
        Cython signature: ScanMode getScanMode()
        Returns the scan mode
        """
        ...
    
    def setScanMode(self, scan_mode: int ) -> None:
        """
        Cython signature: void setScanMode(ScanMode scan_mode)
        Sets the scan mode
        """
        ...
    
    def getZoomScan(self) -> bool:
        """
        Cython signature: bool getZoomScan()
        Returns if this scan is a zoom (enhanced resolution) scan
        """
        ...
    
    def setZoomScan(self, zoom_scan: bool ) -> None:
        """
        Cython signature: void setZoomScan(bool zoom_scan)
        Sets if this scan is a zoom (enhanced resolution) scan
        """
        ...
    
    def getScanWindows(self) -> List[ScanWindow]:
        """
        Cython signature: libcpp_vector[ScanWindow] getScanWindows()
        Returns the m/z scan windows
        """
        ...
    
    def setScanWindows(self, scan_windows: List[ScanWindow] ) -> None:
        """
        Cython signature: void setScanWindows(libcpp_vector[ScanWindow] scan_windows)
        Sets the m/z scan windows
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
    
    def __richcmp__(self, other: InstrumentSettings, op: int) -> Any:
        ... 


class IsobaricChannelInformation:
    """
    Cython implementation of _IsobaricChannelInformation

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IsobaricQuantitationMethod_1_1IsobaricChannelInformation.html>`_
    """
    
    name: Union[bytes, str, String]
    
    id: int
    
    description: Union[bytes, str, String]
    
    center: float
    
    affected_channels: List[int]
    
    @overload
    def __init__(self, name: Union[bytes, str, String] , id_: int , description: Union[bytes, str, String] , center: float , affected_channels: List[int] ) -> None:
        """
        Cython signature: void IsobaricChannelInformation(String name, int id_, String description, double center, libcpp_vector[int] affected_channels)
        """
        ...
    
    @overload
    def __init__(self, in_0: IsobaricChannelInformation ) -> None:
        """
        Cython signature: void IsobaricChannelInformation(IsobaricChannelInformation &)
        """
        ... 


class LightCompound:
    """
    Cython implementation of _LightCompound

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1LightCompound.html>`_
    """
    
    rt: float
    
    drift_time: float
    
    charge: int
    
    sequence: bytes
    
    protein_refs: List[bytes]
    
    peptide_group_label: bytes
    
    id: bytes
    
    sum_formula: bytes
    
    compound_name: bytes
    
    modifications: List[LightModification]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LightCompound()
        """
        ...
    
    @overload
    def __init__(self, in_0: LightCompound ) -> None:
        """
        Cython signature: void LightCompound(LightCompound &)
        """
        ...
    
    def setDriftTime(self, d: float ) -> None:
        """
        Cython signature: void setDriftTime(double d)
        """
        ...
    
    def getDriftTime(self) -> float:
        """
        Cython signature: double getDriftTime()
        """
        ...
    
    def getChargeState(self) -> int:
        """
        Cython signature: int getChargeState()
        """
        ...
    
    def isPeptide(self) -> bool:
        """
        Cython signature: bool isPeptide()
        """
        ...
    
    def setChargeState(self, ch: int ) -> None:
        """
        Cython signature: void setChargeState(int ch)
        """
        ... 


class LightModification:
    """
    Cython implementation of _LightModification

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1LightModification.html>`_
    """
    
    location: int
    
    unimod_id: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LightModification()
        """
        ...
    
    @overload
    def __init__(self, in_0: LightModification ) -> None:
        """
        Cython signature: void LightModification(LightModification &)
        """
        ... 


class LightProtein:
    """
    Cython implementation of _LightProtein

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1LightProtein.html>`_
    """
    
    id: bytes
    
    sequence: bytes
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LightProtein()
        """
        ...
    
    @overload
    def __init__(self, in_0: LightProtein ) -> None:
        """
        Cython signature: void LightProtein(LightProtein &)
        """
        ... 


class LightTargetedExperiment:
    """
    Cython implementation of _LightTargetedExperiment

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1LightTargetedExperiment.html>`_
    """
    
    transitions: List[LightTransition]
    
    compounds: List[LightCompound]
    
    proteins: List[LightProtein]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LightTargetedExperiment()
        """
        ...
    
    @overload
    def __init__(self, in_0: LightTargetedExperiment ) -> None:
        """
        Cython signature: void LightTargetedExperiment(LightTargetedExperiment &)
        """
        ...
    
    def getTransitions(self) -> List[LightTransition]:
        """
        Cython signature: libcpp_vector[LightTransition] getTransitions()
        """
        ...
    
    def getCompounds(self) -> List[LightCompound]:
        """
        Cython signature: libcpp_vector[LightCompound] getCompounds()
        """
        ...
    
    def getProteins(self) -> List[LightProtein]:
        """
        Cython signature: libcpp_vector[LightProtein] getProteins()
        """
        ...
    
    def getCompoundByRef(self, ref: bytes ) -> LightCompound:
        """
        Cython signature: LightCompound getCompoundByRef(libcpp_string & ref)
        """
        ...
    
    def getPeptideByRef(self, ref: bytes ) -> LightCompound:
        """
        Cython signature: LightCompound getPeptideByRef(libcpp_string & ref)
        """
        ... 


class LightTransition:
    """
    Cython implementation of _LightTransition

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1LightTransition.html>`_
    """
    
    transition_name: bytes
    
    peptide_ref: bytes
    
    library_intensity: float
    
    product_mz: float
    
    precursor_mz: float
    
    fragment_charge: int
    
    decoy: bool
    
    detecting_transition: bool
    
    quantifying_transition: bool
    
    identifying_transition: bool
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LightTransition()
        """
        ...
    
    @overload
    def __init__(self, in_0: LightTransition ) -> None:
        """
        Cython signature: void LightTransition(LightTransition &)
        """
        ...
    
    def getProductChargeState(self) -> int:
        """
        Cython signature: int getProductChargeState()
        """
        ...
    
    def isProductChargeStateSet(self) -> bool:
        """
        Cython signature: bool isProductChargeStateSet()
        """
        ...
    
    def getNativeID(self) -> bytes:
        """
        Cython signature: libcpp_string getNativeID()
        """
        ...
    
    def getPeptideRef(self) -> bytes:
        """
        Cython signature: libcpp_string getPeptideRef()
        """
        ...
    
    def getLibraryIntensity(self) -> float:
        """
        Cython signature: double getLibraryIntensity()
        """
        ...
    
    def setLibraryIntensity(self, l: float ) -> None:
        """
        Cython signature: void setLibraryIntensity(double l)
        """
        ...
    
    def getProductMZ(self) -> float:
        """
        Cython signature: double getProductMZ()
        """
        ...
    
    def getPrecursorMZ(self) -> float:
        """
        Cython signature: double getPrecursorMZ()
        """
        ...
    
    def getCompoundRef(self) -> bytes:
        """
        Cython signature: libcpp_string getCompoundRef()
        """
        ...
    
    def setDetectingTransition(self, d: bool ) -> None:
        """
        Cython signature: void setDetectingTransition(bool d)
        """
        ...
    
    def isDetectingTransition(self) -> bool:
        """
        Cython signature: bool isDetectingTransition()
        """
        ...
    
    def setQuantifyingTransition(self, q: bool ) -> None:
        """
        Cython signature: void setQuantifyingTransition(bool q)
        """
        ...
    
    def isQuantifyingTransition(self) -> bool:
        """
        Cython signature: bool isQuantifyingTransition()
        """
        ...
    
    def setIdentifyingTransition(self, i: bool ) -> None:
        """
        Cython signature: void setIdentifyingTransition(bool i)
        """
        ...
    
    def isIdentifyingTransition(self) -> bool:
        """
        Cython signature: bool isIdentifyingTransition()
        """
        ... 


class MRMFeaturePickerFile:
    """
    Cython implementation of _MRMFeaturePickerFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMFeaturePickerFile.html>`_

    _MRMFeaturePickerFile_ loads components and components groups parameters from a .csv file
    
    The structures defined in [MRMFeaturePicker](@ref MRMFeaturePicker) are used
    
    It is required that columns `component_name` and `component_group_name` are present.
    Lines whose `component_name`'s or `component_group_name`'s value is an empty string, will be skipped.
    The class supports the absence of information within other columns.
    
    A reduced example of the expected format (fewer columns are shown here):
    > component_name,component_group_name,TransitionGroupPicker:stop_after_feature,TransitionGroupPicker:PeakPickerChromatogram:sgolay_frame_length
    > arg-L.arg-L_1.Heavy,arg-L,2,15
    > arg-L.arg-L_1.Light,arg-L,2,17
    > orn.orn_1.Heavy,orn,3,21
    > orn.orn_1.Light,orn,3,13
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMFeaturePickerFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMFeaturePickerFile ) -> None:
        """
        Cython signature: void MRMFeaturePickerFile(MRMFeaturePickerFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , cp_list: List[MRMFP_ComponentParams] , cgp_list: List[MRMFP_ComponentGroupParams] ) -> None:
        """
        Cython signature: void load(const String & filename, libcpp_vector[MRMFP_ComponentParams] & cp_list, libcpp_vector[MRMFP_ComponentGroupParams] & cgp_list)
        Loads the file's data and saves it into vectors of `ComponentParams` and `ComponentGroupParams`
        
        The file is expected to contain at least two columns: `component_name` and `component_group_name`. Otherwise,
        an exception is thrown
        
        If a component group (identified by its name) is found multiple times, only the first one is saved
        
        
        :param filename: Path to the .csv input file
        :param cp_list: Component params are saved in this list
        :param cgp_list: Component Group params are saved in this list
        :raises:
          Exception: MissingInformation If the required columns are not found
        :raises:
          Exception: FileNotFound If input file is not found
        """
        ... 


class MSDataAggregatingConsumer:
    """
    Cython implementation of _MSDataAggregatingConsumer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MSDataAggregatingConsumer.html>`_
    """
    
    def __init__(self, in_0: MSDataAggregatingConsumer ) -> None:
        """
        Cython signature: void MSDataAggregatingConsumer(MSDataAggregatingConsumer &)
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


class MzMLFile:
    """
    Cython implementation of _MzMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzMLFile.html>`_
      -- Inherits from ['ProgressLogger']

    File adapter for MzML files
    
    Provides methods to load and store MzML files.
    PeakFileOptions allow to load a reduced subset of the data into an MSExperiment.
    
    See help(MSExperiment) how data is stored after loading.
    See help(PeakFileOptions) for available options.
    
    Usage:
    
    .. code-block:: python
    
      exp = MSExperiment()
      MzMLFile().load("test.mzML", exp)
      spec = []
      for s in exp.getSpectra():
        if s.getMSLevel() != 1:
          spec.append(s)
      exp.setSpectra(spec)
      MzMLFile().store("filtered.mzML", exp)
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MzMLFile ) -> None:
        """
        Cython signature: void MzMLFile(MzMLFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , in_1: MSExperiment ) -> None:
        """
        Cython signature: void load(const String & filename, MSExperiment &)
        Loads from an MzML file. Spectra and chromatograms are sorted by default (this can be disabled using PeakFileOptions)
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , in_1: MSExperiment ) -> None:
        """
        Cython signature: void store(const String & filename, MSExperiment &)
        Stores a MSExperiment in an MzML file
        """
        ...
    
    def storeBuffer(self, output: String , exp: MSExperiment ) -> None:
        """
        Cython signature: void storeBuffer(String & output, MSExperiment exp)
        Stores a map in an output string
        
        
        :param output: An empty string to store the result
        :param exp: Has to be an MSExperiment
        """
        ...
    
    def loadBuffer(self, input: Union[bytes, str, String] , exp: MSExperiment ) -> None:
        """
        Cython signature: void loadBuffer(const String & input, MSExperiment & exp)
        Loads a map from a MzML file stored in a buffer (in memory)
        
        
        :param buffer: The buffer with the data (i.e. string with content of an mzML file)
        :param exp: Is an MSExperiment
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ...
    
    def getOptions(self) -> PeakFileOptions:
        """
        Cython signature: PeakFileOptions getOptions()
        """
        ...
    
    def setOptions(self, in_0: PeakFileOptions ) -> None:
        """
        Cython signature: void setOptions(PeakFileOptions)
        Set PeakFileOptions to perform filtering during loading. E.g., to load only MS1 spectra or meta data only
        """
        ...
    
    def isSemanticallyValid(self, filename: Union[bytes, str, String] , errors: List[bytes] , warnings: List[bytes] ) -> bool:
        """
        Cython signature: bool isSemanticallyValid(const String & filename, StringList & errors, StringList & warnings)
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


class MzMLSqliteHandler:
    """
    Cython implementation of _MzMLSqliteHandler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1MzMLSqliteHandler.html>`_
    """
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] , run_id: int ) -> None:
        """
        Cython signature: void MzMLSqliteHandler(String filename, uint64_t run_id)
        """
        ...
    
    @overload
    def __init__(self, in_0: MzMLSqliteHandler ) -> None:
        """
        Cython signature: void MzMLSqliteHandler(MzMLSqliteHandler &)
        """
        ...
    
    def readExperiment(self, exp: MSExperiment , meta_only: bool ) -> None:
        """
        Cython signature: void readExperiment(MSExperiment & exp, bool meta_only)
        Read an experiment into an MSExperiment structure
        
        
        :param exp: The result data structure
        :param meta_only: Only read the meta data
        """
        ...
    
    def readSpectra(self, exp: List[MSSpectrum] , indices: List[int] , meta_only: bool ) -> None:
        """
        Cython signature: void readSpectra(libcpp_vector[MSSpectrum] & exp, libcpp_vector[int] indices, bool meta_only)
        Read a set of spectra (potentially restricted to a subset)
        
        
        :param exp: The result data structure
        :param indices: A list of indices restricting the resulting spectra only to those specified here
        :param meta_only: Only read the meta data
        """
        ...
    
    def readChromatograms(self, exp: List[MSChromatogram] , indices: List[int] , meta_only: bool ) -> None:
        """
        Cython signature: void readChromatograms(libcpp_vector[MSChromatogram] & exp, libcpp_vector[int] indices, bool meta_only)
        Read a set of chromatograms (potentially restricted to a subset)
        
        
        :param exp: The result data structure
        :param indices: A list of indices restricting the resulting spectra only to those specified here
        :param meta_only: Only read the meta data
        """
        ...
    
    def getNrSpectra(self) -> int:
        """
        Cython signature: size_t getNrSpectra()
        Returns number of spectra in the file, reutrns the number of spectra
        """
        ...
    
    def getNrChromatograms(self) -> int:
        """
        Cython signature: size_t getNrChromatograms()
        Returns the number of chromatograms in the file
        """
        ...
    
    def setConfig(self, write_full_meta: bool , use_lossy_compression: bool , linear_abs_mass_acc: float ) -> None:
        """
        Cython signature: void setConfig(bool write_full_meta, bool use_lossy_compression, double linear_abs_mass_acc)
        Sets file configuration
        
        
        :param write_full_meta: Whether to write a complete mzML meta data structure into the RUN_EXTRA field (allows complete recovery of the input file)
        :param use_lossy_compression: Whether to use lossy compression (ms numpress)
        :param linear_abs_mass_acc: Accepted loss in mass accuracy (absolute m/z, in Th)
        """
        ...
    
    def getSpectraIndicesbyRT(self, RT: float , deltaRT: float , indices: List[int] ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] getSpectraIndicesbyRT(double RT, double deltaRT, libcpp_vector[int] indices)
        Returns spectral indices around a specific retention time
        
        :param RT: The retention time
        :param deltaRT: Tolerance window around RT (if less or equal than zero, only the first spectrum *after* RT is returned)
        :param indices: Spectra to consider (if empty, all spectra are considered)
        :return: The indices of the spectra within RT +/- deltaRT
        """
        ...
    
    def writeExperiment(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void writeExperiment(MSExperiment exp)
        Write an MSExperiment to disk
        """
        ...
    
    def createTables(self) -> None:
        """
        Cython signature: void createTables()
        Create data tables for a new file
        """
        ...
    
    def writeSpectra(self, spectra: List[MSSpectrum] ) -> None:
        """
        Cython signature: void writeSpectra(libcpp_vector[MSSpectrum] spectra)
        Writes a set of spectra to disk
        """
        ...
    
    def writeChromatograms(self, chroms: List[MSChromatogram] ) -> None:
        """
        Cython signature: void writeChromatograms(libcpp_vector[MSChromatogram] chroms)
        Writes a set of chromatograms to disk
        """
        ...
    
    def writeRunLevelInformation(self, exp: MSExperiment , write_full_meta: bool ) -> None:
        """
        Cython signature: void writeRunLevelInformation(MSExperiment exp, bool write_full_meta)
        Write the run-level information for an experiment into tables
        
        This is a low level function, do not call this function unless you know what you are doing
        
        
        :param exp: The result data structure
        :param meta_only: Only read the meta data
        """
        ...
    
    def getRunID(self) -> int:
        """
        Cython signature: uint64_t getRunID()
        Extract the `RUN` ID from the sqMass file
        """
        ... 


class MzTab:
    """
    Cython implementation of _MzTab

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzTab.html>`_

    Data model of MzTab files
    
    Please see the official MzTab specification at https://code.google.com/p/mztab/
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzTab()
        """
        ...
    
    @overload
    def __init__(self, in_0: MzTab ) -> None:
        """
        Cython signature: void MzTab(MzTab &)
        """
        ... 


class NASequence:
    """
    Cython implementation of _NASequence

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1NASequence.html>`_

    Representation of an RNA sequence
    This class represents nucleic acid sequences in OpenMS. An NASequence
    instance primarily contains a sequence of ribonucleotides.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void NASequence()
        """
        ...
    
    @overload
    def __init__(self, in_0: NASequence ) -> None:
        """
        Cython signature: void NASequence(NASequence &)
        """
        ...
    
    def getSequence(self) -> List[Ribonucleotide]:
        """
        Cython signature: libcpp_vector[const Ribonucleotide *] getSequence()
        """
        ...
    
    def __getitem__(self, index: int ) -> Ribonucleotide:
        """
        Cython signature: const Ribonucleotide * operator[](size_t index)
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        Check if sequence is empty
        """
        ...
    
    def setSequence(self, seq: List[Ribonucleotide] ) -> None:
        """
        Cython signature: void setSequence(const libcpp_vector[const Ribonucleotide *] & seq)
        """
        ...
    
    def toString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the peptide as string with modifications embedded in brackets
        """
        ...
    
    def setFivePrimeMod(self, modification: Ribonucleotide ) -> None:
        """
        Cython signature: void setFivePrimeMod(const Ribonucleotide * modification)
        Sets the 5' modification
        """
        ...
    
    def getFivePrimeMod(self) -> Ribonucleotide:
        """
        Cython signature: const Ribonucleotide * getFivePrimeMod()
        Returns the name (ID) of the N-terminal modification, or an empty string if none is set
        """
        ...
    
    def setThreePrimeMod(self, modification: Ribonucleotide ) -> None:
        """
        Cython signature: void setThreePrimeMod(const Ribonucleotide * modification)
        Sets the 3' modification
        """
        ...
    
    def getThreePrimeMod(self) -> Ribonucleotide:
        """
        Cython signature: const Ribonucleotide * getThreePrimeMod()
        """
        ...
    
    def get(self, index: int ) -> Ribonucleotide:
        """
        Cython signature: const Ribonucleotide * get(size_t index)
        Returns the residue at position index
        """
        ...
    
    def set(self, index: int , r: Ribonucleotide ) -> None:
        """
        Cython signature: void set(size_t index, const Ribonucleotide * r)
        Sets the residue at position index
        """
        ...
    
    @overload
    def getFormula(self, ) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getFormula()
        Returns the formula of the peptide
        """
        ...
    
    @overload
    def getFormula(self, type_: int , charge: int ) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getFormula(NASFragmentType type_, int charge)
        """
        ...
    
    @overload
    def getAverageWeight(self, ) -> float:
        """
        Cython signature: double getAverageWeight()
        Returns the average weight of the peptide
        """
        ...
    
    @overload
    def getAverageWeight(self, type_: int , charge: int ) -> float:
        """
        Cython signature: double getAverageWeight(NASFragmentType type_, int charge)
        """
        ...
    
    @overload
    def getMonoWeight(self, ) -> float:
        """
        Cython signature: double getMonoWeight()
        Returns the mono isotopic weight of the peptide
        """
        ...
    
    @overload
    def getMonoWeight(self, type_: int , charge: int ) -> float:
        """
        Cython signature: double getMonoWeight(NASFragmentType type_, int charge)
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        Returns the number of residues
        """
        ...
    
    def getPrefix(self, length: int ) -> NASequence:
        """
        Cython signature: NASequence getPrefix(size_t length)
        Returns a peptide sequence of the first index residues
        """
        ...
    
    def getSuffix(self, length: int ) -> NASequence:
        """
        Cython signature: NASequence getSuffix(size_t length)
        Returns a peptide sequence of the last index residues
        """
        ...
    
    def getSubsequence(self, start: int , length: int ) -> NASequence:
        """
        Cython signature: NASequence getSubsequence(size_t start, size_t length)
        Returns a peptide sequence of number residues, beginning at position index
        """
        ...
    
    def __str__(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the peptide as string with modifications embedded in brackets
        """
        ...
    
    def __richcmp__(self, other: NASequence, op: int) -> Any:
        ...
    NASFragmentType : __NASFragmentType
    
    fromString: __static_NASequence_fromString 


class OMSSAXMLFile:
    """
    Cython implementation of _OMSSAXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OMSSAXMLFile.html>`_
      -- Inherits from ['XMLFile']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void OMSSAXMLFile()
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , protein_identification: ProteinIdentification , id_data: List[PeptideIdentification] , load_proteins: bool , load_empty_hits: bool ) -> None:
        """
        Cython signature: void load(const String & filename, ProteinIdentification & protein_identification, libcpp_vector[PeptideIdentification] & id_data, bool load_proteins, bool load_empty_hits)
        Loads data from a OMSSAXML file
        
        
        :param filename: The file to be loaded
        :param protein_identification: Protein identifications belonging to the whole experiment
        :param id_data: The identifications with m/z and RT
        :param load_proteins: If this flag is set to false, the protein identifications are not loaded
        :param load_empty_hits: Many spectra will not return a hit. Report empty peptide identifications?
        """
        ...
    
    def setModificationDefinitionsSet(self, rhs: ModificationDefinitionsSet ) -> None:
        """
        Cython signature: void setModificationDefinitionsSet(ModificationDefinitionsSet rhs)
        Sets the valid modifications
        """
        ...
    
    def getVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVersion()
        Return the version of the schema
        """
        ... 


class OSChromatogramMeta:
    """
    Cython implementation of _OSChromatogramMeta

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1OSChromatogramMeta.html>`_
    """
    
    index: int
    
    id: bytes
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OSChromatogramMeta()
        """
        ...
    
    @overload
    def __init__(self, in_0: OSChromatogramMeta ) -> None:
        """
        Cython signature: void OSChromatogramMeta(OSChromatogramMeta &)
        """
        ... 


class ParamEntry:
    """
    Cython implementation of _ParamEntry

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Param_1_1ParamEntry.html>`_
    """
    
    name: bytes
    
    description: bytes
    
    value: Union[int, float, bytes, str, List[int], List[float], List[bytes]]
    
    tags: Set[bytes]
    
    valid_strings: List[bytes]
    
    max_float: float
    
    min_float: float
    
    max_int: int
    
    min_int: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ParamEntry()
        """
        ...
    
    @overload
    def __init__(self, in_0: ParamEntry ) -> None:
        """
        Cython signature: void ParamEntry(ParamEntry &)
        """
        ...
    
    @overload
    def __init__(self, n: bytes , v: Union[int, float, bytes, str, List[int], List[float], List[bytes]] , d: bytes , t: List[bytes] ) -> None:
        """
        Cython signature: void ParamEntry(libcpp_string n, ParamValue v, libcpp_string d, libcpp_vector[libcpp_string] t)
        """
        ...
    
    @overload
    def __init__(self, n: bytes , v: Union[int, float, bytes, str, List[int], List[float], List[bytes]] , d: bytes ) -> None:
        """
        Cython signature: void ParamEntry(libcpp_string n, ParamValue v, libcpp_string d)
        """
        ...
    
    def __richcmp__(self, other: ParamEntry, op: int) -> Any:
        ... 


class PeakWidthEstimator:
    """
    Cython implementation of _PeakWidthEstimator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeakWidthEstimator.html>`_

    Rough estimation of the peak width at m/z
    
    Based on the peaks of the dataset (peak position & width) and the peak
    boundaries as reported by the PeakPickerHiRes, the typical peak width is
    estimated for arbitrary m/z using a spline interpolationThis struct can be used to store both peak or feature indices`
    """
    
    @overload
    def __init__(self, in_0: PeakWidthEstimator ) -> None:
        """
        Cython signature: void PeakWidthEstimator(PeakWidthEstimator &)
        """
        ...
    
    @overload
    def __init__(self, exp_picked: MSExperiment , boundaries: List[List[PeakBoundary]] ) -> None:
        """
        Cython signature: void PeakWidthEstimator(MSExperiment exp_picked, libcpp_vector[libcpp_vector[PeakBoundary]] & boundaries)
        """
        ...
    
    def getPeakWidth(self, mz: float ) -> float:
        """
        Cython signature: double getPeakWidth(double mz)
        Returns the estimated peak width at m/z
        """
        ... 


class ProbablePhosphoSites:
    """
    Cython implementation of _ProbablePhosphoSites

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProbablePhosphoSites.html>`_
    """
    
    first: int
    
    second: int
    
    seq_1: int
    
    seq_2: int
    
    peak_depth: int
    
    AScore: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProbablePhosphoSites()
        """
        ...
    
    @overload
    def __init__(self, in_0: ProbablePhosphoSites ) -> None:
        """
        Cython signature: void ProbablePhosphoSites(ProbablePhosphoSites &)
        """
        ... 


class ProteaseDB:
    """
    Cython implementation of _ProteaseDB

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProteaseDB.html>`_
    """
    
    def getEnzyme(self, name: Union[bytes, str, String] ) -> DigestionEnzymeProtein:
        """
        Cython signature: const DigestionEnzymeProtein * getEnzyme(const String & name)
        """
        ...
    
    def getEnzymeByRegEx(self, cleavage_regex: Union[bytes, str, String] ) -> DigestionEnzymeProtein:
        """
        Cython signature: const DigestionEnzymeProtein * getEnzymeByRegEx(const String & cleavage_regex)
        """
        ...
    
    def getAllNames(self, all_names: List[bytes] ) -> None:
        """
        Cython signature: void getAllNames(libcpp_vector[String] & all_names)
        """
        ...
    
    def getAllXTandemNames(self, all_names: List[bytes] ) -> None:
        """
        Cython signature: void getAllXTandemNames(libcpp_vector[String] & all_names)
        Returns all the enzyme names available for XTandem
        """
        ...
    
    def getAllOMSSANames(self, all_names: List[bytes] ) -> None:
        """
        Cython signature: void getAllOMSSANames(libcpp_vector[String] & all_names)
        Returns all the enzyme names available for OMSSA
        """
        ...
    
    def getAllCometNames(self, all_names: List[bytes] ) -> None:
        """
        Cython signature: void getAllCometNames(libcpp_vector[String] & all_names)
        Returns all the enzyme names available for Comet
        """
        ...
    
    def getAllMSGFNames(self, all_names: List[bytes] ) -> None:
        """
        Cython signature: void getAllMSGFNames(libcpp_vector[String] & all_names)
        Returns all the enzyme names available for MSGFPlus
        """
        ...
    
    def hasEnzyme(self, name: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasEnzyme(const String & name)
        """
        ...
    
    def hasRegEx(self, cleavage_regex: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasRegEx(const String & cleavage_regex)
        """
        ... 


class ProteinGroup:
    """
    Cython implementation of _ProteinGroup

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProteinGroup.html>`_
    """
    
    probability: float
    
    accessions: List[bytes]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProteinGroup()
        """
        ...
    
    @overload
    def __init__(self, in_0: ProteinGroup ) -> None:
        """
        Cython signature: void ProteinGroup(ProteinGroup &)
        """
        ... 


class ProteinIdentification:
    """
    Cython implementation of _ProteinIdentification

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProteinIdentification.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProteinIdentification()
        """
        ...
    
    @overload
    def __init__(self, in_0: ProteinIdentification ) -> None:
        """
        Cython signature: void ProteinIdentification(ProteinIdentification &)
        """
        ...
    
    def getHits(self) -> List[ProteinHit]:
        """
        Cython signature: libcpp_vector[ProteinHit] getHits()
        Returns the protein hits
        """
        ...
    
    def insertHit(self, input: ProteinHit ) -> None:
        """
        Cython signature: void insertHit(ProteinHit input)
        Appends a protein hit
        """
        ...
    
    def setHits(self, hits: List[ProteinHit] ) -> None:
        """
        Cython signature: void setHits(libcpp_vector[ProteinHit] hits)
        Sets the protein hits
        """
        ...
    
    def getProteinGroups(self) -> List[ProteinGroup]:
        """
        Cython signature: libcpp_vector[ProteinGroup] getProteinGroups()
        Returns the protein groups
        """
        ...
    
    def insertProteinGroup(self, group: ProteinGroup ) -> None:
        """
        Cython signature: void insertProteinGroup(ProteinGroup group)
        Appends a new protein group
        """
        ...
    
    def getIndistinguishableProteins(self) -> List[ProteinGroup]:
        """
        Cython signature: libcpp_vector[ProteinGroup] getIndistinguishableProteins()
        Returns the indistinguishable proteins
        """
        ...
    
    def insertIndistinguishableProteins(self, group: ProteinGroup ) -> None:
        """
        Cython signature: void insertIndistinguishableProteins(ProteinGroup group)
        Appends new indistinguishable proteins
        """
        ...
    
    def getSignificanceThreshold(self) -> float:
        """
        Cython signature: double getSignificanceThreshold()
        Returns the protein significance threshold value
        """
        ...
    
    def setSignificanceThreshold(self, value: float ) -> None:
        """
        Cython signature: void setSignificanceThreshold(double value)
        Sets the protein significance threshold value
        """
        ...
    
    def getScoreType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getScoreType()
        Returns the protein score type
        """
        ...
    
    def setScoreType(self, type: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setScoreType(String type)
        Sets the protein score type
        """
        ...
    
    def isHigherScoreBetter(self) -> bool:
        """
        Cython signature: bool isHigherScoreBetter()
        Returns true if a higher score represents a better score
        """
        ...
    
    def setHigherScoreBetter(self, higher_is_better: bool ) -> None:
        """
        Cython signature: void setHigherScoreBetter(bool higher_is_better)
        Sets the orientation of the score (is higher better?)
        """
        ...
    
    def sort(self) -> None:
        """
        Cython signature: void sort()
        Sorts the protein hits according to their score
        """
        ...
    
    def assignRanks(self) -> None:
        """
        Cython signature: void assignRanks()
        Sorts the protein hits by score and assigns ranks (best score has rank 1)
        """
        ...
    
    def computeCoverage(self, pep_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void computeCoverage(libcpp_vector[PeptideIdentification] pep_ids)
        Compute the coverage (in percent) of all ProteinHits given PeptideHits
        """
        ...
    
    def getDateTime(self) -> DateTime:
        """
        Cython signature: DateTime getDateTime()
        Returns the date of the protein identification run
        """
        ...
    
    def setDateTime(self, date: DateTime ) -> None:
        """
        Cython signature: void setDateTime(DateTime date)
        Sets the date of the protein identification run
        """
        ...
    
    def setSearchEngine(self, search_engine: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSearchEngine(String search_engine)
        Sets the search engine type
        """
        ...
    
    def getSearchEngine(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSearchEngine()
        Returns the type of search engine used
        """
        ...
    
    def setSearchEngineVersion(self, search_engine_version: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSearchEngineVersion(String search_engine_version)
        Sets the search engine version
        """
        ...
    
    def getSearchEngineVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSearchEngineVersion()
        Returns the search engine version
        """
        ...
    
    def setSearchParameters(self, search_parameters: SearchParameters ) -> None:
        """
        Cython signature: void setSearchParameters(SearchParameters search_parameters)
        Sets the search parameters
        """
        ...
    
    def getSearchParameters(self) -> SearchParameters:
        """
        Cython signature: SearchParameters getSearchParameters()
        Returns the search parameters
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        Returns the identifier
        """
        ...
    
    def setIdentifier(self, id_: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(String id_)
        Sets the identifier
        """
        ...
    
    @overload
    def setPrimaryMSRunPath(self, s: List[bytes] ) -> None:
        """
        Cython signature: void setPrimaryMSRunPath(StringList & s)
        Set the file paths to the primary MS runs (usually the mzML files obtained after data conversion from raw files)
        
        
        :param raw: Store paths to the raw files (or equivalent) rather than mzMLs
        """
        ...
    
    @overload
    def setPrimaryMSRunPath(self, s: List[bytes] , raw: bool ) -> None:
        """
        Cython signature: void setPrimaryMSRunPath(StringList & s, bool raw)
        """
        ...
    
    @overload
    def addPrimaryMSRunPath(self, s: List[bytes] ) -> None:
        """
        Cython signature: void addPrimaryMSRunPath(StringList & s)
        """
        ...
    
    @overload
    def addPrimaryMSRunPath(self, s: List[bytes] , raw: bool ) -> None:
        """
        Cython signature: void addPrimaryMSRunPath(StringList & s, bool raw)
        """
        ...
    
    @overload
    def getPrimaryMSRunPath(self, output: List[bytes] ) -> None:
        """
        Cython signature: void getPrimaryMSRunPath(StringList & output)
        """
        ...
    
    @overload
    def getPrimaryMSRunPath(self, output: List[bytes] , raw: bool ) -> None:
        """
        Cython signature: void getPrimaryMSRunPath(StringList & output, bool raw)
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
    
    def __richcmp__(self, other: ProteinIdentification, op: int) -> Any:
        ...
    PeakMassType : __PeakMassType 


class RNaseDigestion:
    """
    Cython implementation of _RNaseDigestion

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1RNaseDigestion.html>`_
      -- Inherits from ['EnzymaticDigestion']

    Class for the enzymatic digestion of RNA
    
    Usage:
    
    .. code-block:: python
    
          from pyopenms import *
          oligo = NASequence.fromString("pAUGUCGCAG");
    
          dig = RNaseDigestion()
          dig.setEnzyme("RNase_T1")
    
          result = []
          dig.digest(oligo, result)
          for fragment in result:
            print (fragment)
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RNaseDigestion()
        """
        ...
    
    @overload
    def __init__(self, in_0: RNaseDigestion ) -> None:
        """
        Cython signature: void RNaseDigestion(RNaseDigestion &)
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
    def digest(self, rna: NASequence , output: List[NASequence] ) -> None:
        """
        Cython signature: void digest(NASequence & rna, libcpp_vector[NASequence] & output)
        """
        ...
    
    @overload
    def digest(self, rna: NASequence , output: List[NASequence] , min_length: int , max_length: int ) -> None:
        """
        Cython signature: void digest(NASequence & rna, libcpp_vector[NASequence] & output, size_t min_length, size_t max_length)
        Performs the enzymatic digestion of a (potentially modified) RNA
        
        :param rna: Sequence to digest
        :param output: Digestion productsq
        :param min_length: Minimal length of reported products
        :param max_length: Maximal length of reported products (0 = no restriction)
        :returns: Number of discarded digestion products (which are not matching length restrictions)
        Performs the enzymatic digestion of all RNA parent molecules in IdentificationData (id_data)
        
        :param id_data: IdentificationData object which includes sequences to digest
        :param min_length: Minimal length of reported products
        :param max_length: Maximal length of reported products (0 = no restriction)
        :returns: Number of discarded digestion products (which are not matching length restrictions)
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


class RansacModelLinear:
    """
    Cython implementation of _RansacModelLinear

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1RansacModelLinear.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RansacModelLinear()
        """
        ...
    
    @overload
    def __init__(self, in_0: RansacModelLinear ) -> None:
        """
        Cython signature: void RansacModelLinear(RansacModelLinear &)
        """
        ... 


class ReactionMonitoringTransition:
    """
    Cython implementation of _ReactionMonitoringTransition

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ReactionMonitoringTransition.html>`_
      -- Inherits from ['CVTermList']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ReactionMonitoringTransition()
        """
        ...
    
    @overload
    def __init__(self, in_0: ReactionMonitoringTransition ) -> None:
        """
        Cython signature: void ReactionMonitoringTransition(ReactionMonitoringTransition &)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        """
        ...
    
    def getNativeID(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNativeID()
        """
        ...
    
    def getPeptideRef(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getPeptideRef()
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        """
        ...
    
    def setNativeID(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNativeID(String name)
        """
        ...
    
    def setPeptideRef(self, peptide_ref: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setPeptideRef(String peptide_ref)
        """
        ...
    
    def getProductMZ(self) -> float:
        """
        Cython signature: double getProductMZ()
        """
        ...
    
    def setProductMZ(self, in_0: float ) -> None:
        """
        Cython signature: void setProductMZ(double)
        """
        ...
    
    def getPrecursorMZ(self) -> float:
        """
        Cython signature: double getPrecursorMZ()
        Returns the precursor mz (Q1 value)
        """
        ...
    
    def setPrecursorMZ(self, in_0: float ) -> None:
        """
        Cython signature: void setPrecursorMZ(double)
        Sets the precursor mz (Q1 value)
        """
        ...
    
    def getDecoyTransitionType(self) -> int:
        """
        Cython signature: DecoyTransitionType getDecoyTransitionType()
        Returns the type of transition (target or decoy)
        """
        ...
    
    def setCompoundRef(self, compound_ref: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCompoundRef(const String & compound_ref)
        """
        ...
    
    def getCompoundRef(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCompoundRef()
        """
        ...
    
    def hasPrecursorCVTerms(self) -> bool:
        """
        Cython signature: bool hasPrecursorCVTerms()
        Returns true if precursor CV Terms exist (means it is safe to call getPrecursorCVTermList)
        """
        ...
    
    def setPrecursorCVTermList(self, list_: CVTermList ) -> None:
        """
        Cython signature: void setPrecursorCVTermList(CVTermList & list_)
        Sets a list of precursor CV Terms
        """
        ...
    
    def addPrecursorCVTerm(self, cv_term: CVTerm ) -> None:
        """
        Cython signature: void addPrecursorCVTerm(CVTerm & cv_term)
        Adds precursor CV Term
        """
        ...
    
    def getPrecursorCVTermList(self) -> CVTermList:
        """
        Cython signature: CVTermList getPrecursorCVTermList()
        Obtains the list of CV Terms for the precursor
        """
        ...
    
    def addProductCVTerm(self, cv_term: CVTerm ) -> None:
        """
        Cython signature: void addProductCVTerm(CVTerm & cv_term)
        """
        ...
    
    def getIntermediateProducts(self) -> List[TraMLProduct]:
        """
        Cython signature: libcpp_vector[TraMLProduct] getIntermediateProducts()
        """
        ...
    
    def addIntermediateProduct(self, product: TraMLProduct ) -> None:
        """
        Cython signature: void addIntermediateProduct(TraMLProduct product)
        """
        ...
    
    def setIntermediateProducts(self, products: List[TraMLProduct] ) -> None:
        """
        Cython signature: void setIntermediateProducts(libcpp_vector[TraMLProduct] & products)
        """
        ...
    
    def setProduct(self, product: TraMLProduct ) -> None:
        """
        Cython signature: void setProduct(TraMLProduct product)
        """
        ...
    
    def getProduct(self) -> TraMLProduct:
        """
        Cython signature: TraMLProduct getProduct()
        """
        ...
    
    def setRetentionTime(self, rt: RetentionTime ) -> None:
        """
        Cython signature: void setRetentionTime(RetentionTime rt)
        """
        ...
    
    def getRetentionTime(self) -> RetentionTime:
        """
        Cython signature: RetentionTime getRetentionTime()
        """
        ...
    
    def setPrediction(self, prediction: Prediction ) -> None:
        """
        Cython signature: void setPrediction(Prediction & prediction)
        Sets prediction
        """
        ...
    
    def addPredictionTerm(self, prediction: CVTerm ) -> None:
        """
        Cython signature: void addPredictionTerm(CVTerm & prediction)
        Adds prediction term
        """
        ...
    
    def hasPrediction(self) -> bool:
        """
        Cython signature: bool hasPrediction()
        Returns true if a Prediction object exists (means it is safe to call getPrediction)
        """
        ...
    
    def getPrediction(self) -> Prediction:
        """
        Cython signature: Prediction getPrediction()
        Obtains the Prediction object
        """
        ...
    
    def setDecoyTransitionType(self, d: int ) -> None:
        """
        Cython signature: void setDecoyTransitionType(DecoyTransitionType & d)
        Sets the type of transition (target or decoy)
        """
        ...
    
    def getLibraryIntensity(self) -> float:
        """
        Cython signature: double getLibraryIntensity()
        Returns the library intensity (ion count or normalized ion count from a spectral library)
        """
        ...
    
    def setLibraryIntensity(self, intensity: float ) -> None:
        """
        Cython signature: void setLibraryIntensity(double intensity)
        Sets the library intensity (ion count or normalized ion count from a spectral library)
        """
        ...
    
    def getProductChargeState(self) -> int:
        """
        Cython signature: int getProductChargeState()
        Returns the charge state of the product
        """
        ...
    
    def isProductChargeStateSet(self) -> bool:
        """
        Cython signature: bool isProductChargeStateSet()
        Returns true if charge state of product is already set
        """
        ...
    
    def isDetectingTransition(self) -> bool:
        """
        Cython signature: bool isDetectingTransition()
        """
        ...
    
    def setDetectingTransition(self, val: bool ) -> None:
        """
        Cython signature: void setDetectingTransition(bool val)
        """
        ...
    
    def isIdentifyingTransition(self) -> bool:
        """
        Cython signature: bool isIdentifyingTransition()
        """
        ...
    
    def setIdentifyingTransition(self, val: bool ) -> None:
        """
        Cython signature: void setIdentifyingTransition(bool val)
        """
        ...
    
    def isQuantifyingTransition(self) -> bool:
        """
        Cython signature: bool isQuantifyingTransition()
        """
        ...
    
    def setQuantifyingTransition(self, val: bool ) -> None:
        """
        Cython signature: void setQuantifyingTransition(bool val)
        """
        ...
    
    def setCVTerms(self, terms: List[CVTerm] ) -> None:
        """
        Cython signature: void setCVTerms(libcpp_vector[CVTerm] & terms)
        Sets the CV terms
        """
        ...
    
    def replaceCVTerm(self, term: CVTerm ) -> None:
        """
        Cython signature: void replaceCVTerm(CVTerm & term)
        Replaces the specified CV term
        """
        ...
    
    def replaceCVTerms(self, cv_terms: List[CVTerm] , accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void replaceCVTerms(libcpp_vector[CVTerm] cv_terms, String accession)
        """
        ...
    
    def consumeCVTerms(self, cv_term_map: Dict[bytes,List[CVTerm]] ) -> None:
        """
        Cython signature: void consumeCVTerms(libcpp_map[String,libcpp_vector[CVTerm]] cv_term_map)
        Merges the given map into the member map, no duplicate checking
        """
        ...
    
    def getCVTerms(self) -> Dict[bytes,List[CVTerm]]:
        """
        Cython signature: libcpp_map[String,libcpp_vector[CVTerm]] getCVTerms()
        Returns the accession string of the term
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
        Cython signature: bool hasCVTerm(String accession)
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
    
    def __richcmp__(self, other: ReactionMonitoringTransition, op: int) -> Any:
        ... 


class SearchParameters:
    """
    Cython implementation of _SearchParameters

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SearchParameters.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    db: Union[bytes, str, String]
    
    db_version: Union[bytes, str, String]
    
    taxonomy: Union[bytes, str, String]
    
    charges: Union[bytes, str, String]
    
    mass_type: int
    
    fixed_modifications: List[bytes]
    
    variable_modifications: List[bytes]
    
    missed_cleavages: int
    
    fragment_mass_tolerance: float
    
    fragment_mass_tolerance_ppm: bool
    
    precursor_mass_tolerance: float
    
    precursor_mass_tolerance_ppm: bool
    
    digestion_enzyme: DigestionEnzymeProtein
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SearchParameters()
        """
        ...
    
    @overload
    def __init__(self, in_0: SearchParameters ) -> None:
        """
        Cython signature: void SearchParameters(SearchParameters &)
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
    
    def __richcmp__(self, other: SearchParameters, op: int) -> Any:
        ... 


class SimplePeak:
    """
    Cython implementation of _SimplePeak

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SimplePeak.html>`_
    """
    
    mz: float
    
    charge: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SimplePeak()
        A simple struct to represent peaks with mz and charge and sort them easily
        """
        ...
    
    @overload
    def __init__(self, mz: float , charge: int ) -> None:
        """
        Cython signature: void SimplePeak(double mz, int charge)
        """
        ...
    
    @overload
    def __init__(self, in_0: SimplePeak ) -> None:
        """
        Cython signature: void SimplePeak(SimplePeak &)
        """
        ... 


class SimpleTSGXLMS:
    """
    Cython implementation of _SimpleTSGXLMS

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SimpleTSGXLMS.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SimpleTSGXLMS()
        Generates theoretical spectra for cross-linked peptides
        
        The spectra this class generates are vectors of SimplePeaks
        This class generates the same peak types as TheoreticalSpectrumGeneratorXLMS
        and the interface is very similar, but it is simpler and faster
        SimplePeak only contains an mz value and a charge. No intensity values
        or String annotations or other additional DataArrays are generated
        """
        ...
    
    @overload
    def __init__(self, in_0: SimpleTSGXLMS ) -> None:
        """
        Cython signature: void SimpleTSGXLMS(SimpleTSGXLMS &)
        """
        ...
    
    def getLinearIonSpectrum(self, spectrum: List[SimplePeak] , peptide: AASequence , link_pos: int , charge: int , link_pos_2: int ) -> None:
        """
        Cython signature: void getLinearIonSpectrum(libcpp_vector[SimplePeak] & spectrum, AASequence peptide, size_t link_pos, int charge, size_t link_pos_2)
        Generates fragment ions not containing the cross-linker for one peptide
        
        B-ions are generated from the beginning of the peptide up to the first linked position,
        y-ions are generated from the second linked position up the end of the peptide
        If link_pos_2 is 0, a mono-link or cross-link is assumed and the second position is the same as the first position
        For a loop-link two different positions can be set and link_pos_2 must be larger than link_pos
        The generated ion types and other additional settings are determined by the tool parameters
        
        :param spectrum: The spectrum to which the new peaks are added. Does not have to be empty, the generated peaks will be pushed onto it
        :param peptide: The peptide to fragment
        :param link_pos: The position of the cross-linker on the given peptide
        :param charge: The maximal charge of the ions
        :param link_pos_2: A second position for the linker, in case it is a loop link
        """
        ...
    
    @overload
    def getXLinkIonSpectrum(self, spectrum: List[SimplePeak] , peptide: AASequence , link_pos: int , precursor_mass: float , mincharge: int , maxcharge: int , link_pos_2: int ) -> None:
        """
        Cython signature: void getXLinkIonSpectrum(libcpp_vector[SimplePeak] & spectrum, AASequence peptide, size_t link_pos, double precursor_mass, int mincharge, int maxcharge, size_t link_pos_2)
        Generates fragment ions containing the cross-linker for one peptide
        
        B-ions are generated from the first linked position up to the end of the peptide,
        y-ions are generated from the beginning of the peptide up to the second linked position
        If link_pos_2 is 0, a mono-link or cross-link is assumed and the second position is the same as the first position
        For a loop-link two different positions can be set and link_pos_2 must be larger than link_pos
        Since in the case of a cross-link a whole second peptide is attached to the other side of the cross-link,
        a precursor mass for the two peptides and the linker is needed
        In the case of a loop link the precursor mass is the mass of the only peptide and the linker
        Although this function is more general, currently it is mainly used for loop-links and mono-links,
        because residues in the second, unknown peptide cannot be considered for possible neutral losses
        The generated ion types and other additional settings are determined by the tool parameters
        
        :param spectrum: The spectrum to which the new peaks are added. Does not have to be empty, the generated peaks will be pushed onto it
        :param peptide: The peptide to fragment
        :param link_pos: The position of the cross-linker on the given peptide
        :param precursor_mass: The mass of the whole cross-link candidate or the precursor mass of the experimental MS2 spectrum
        :param mincharge: The minimal charge of the ions
        :param maxcharge: The maximal charge of the ions, it should be the precursor charge and is used to generate precursor ion peaks
        :param link_pos_2: A second position for the linker, in case it is a loop link
        """
        ...
    
    @overload
    def getXLinkIonSpectrum(self, spectrum: List[SimplePeak] , crosslink: ProteinProteinCrossLink , frag_alpha: bool , mincharge: int , maxcharge: int ) -> None:
        """
        Cython signature: void getXLinkIonSpectrum(libcpp_vector[SimplePeak] & spectrum, ProteinProteinCrossLink crosslink, bool frag_alpha, int mincharge, int maxcharge)
        Generates fragment ions containing the cross-linker for a pair of peptides
        
        B-ions are generated from the first linked position up to the end of the peptide,
        y-ions are generated from the beginning of the peptide up to the second linked position
        This function generates neutral loss ions by considering both linked peptides
        Only one of the peptides, decided by @frag_alpha, is fragmented
        This simplifies the function, but it has to be called twice to get all fragments of a peptide pair
        The generated ion types and other additional settings are determined by the tool parameters
        This function is not suitable to generate fragments for mono-links or loop-links
        
        :param spectrum: The spectrum to which the new peaks are added. Does not have to be empty, the generated peaks will be pushed onto it
        :param crosslink: ProteinProteinCrossLink to be fragmented
        :param link_pos: The position of the cross-linker on the given peptide
        :param precursor_mass: The mass of the whole cross-link candidate or the precursor mass of the experimental MS2 spectrum
        :param frag_alpha: True, if the fragmented peptide is the Alpha peptide
        :param mincharge: The minimal charge of the ions
        :param maxcharge: The maximal charge of the ions, it should be the precursor charge and is used to generate precursor ion peaks
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


class SiriusExportAlgorithm:
    """
    Cython implementation of _SiriusExportAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SiriusExportAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SiriusExportAlgorithm()
        """
        ...
    
    @overload
    def __init__(self, in_0: SiriusExportAlgorithm ) -> None:
        """
        Cython signature: void SiriusExportAlgorithm(SiriusExportAlgorithm &)
        """
        ...
    
    def isFeatureOnly(self) -> bool:
        """
        Cython signature: bool isFeatureOnly()
        """
        ...
    
    def getFilterByNumMassTraces(self) -> int:
        """
        Cython signature: unsigned int getFilterByNumMassTraces()
        """
        ...
    
    def getPrecursorMzTolerance(self) -> float:
        """
        Cython signature: double getPrecursorMzTolerance()
        """
        ...
    
    def getPrecursorRtTolerance(self) -> float:
        """
        Cython signature: double getPrecursorRtTolerance()
        """
        ...
    
    def precursorMzToleranceUnitIsPPM(self) -> bool:
        """
        Cython signature: bool precursorMzToleranceUnitIsPPM()
        """
        ...
    
    def isNoMasstraceInfoIsotopePattern(self) -> bool:
        """
        Cython signature: bool isNoMasstraceInfoIsotopePattern()
        """
        ...
    
    def getIsotopePatternIterations(self) -> int:
        """
        Cython signature: int getIsotopePatternIterations()
        """
        ...
    
    def preprocessing(self, featureXML_path: Union[bytes, str, String] , spectra: MSExperiment , feature_mapping_info: FeatureMapping_FeatureMappingInfo , feature_ms2_indices: FeatureMapping_FeatureToMs2Indices ) -> None:
        """
        Cython signature: void preprocessing(const String & featureXML_path, MSExperiment & spectra, FeatureMapping_FeatureMappingInfo & feature_mapping_info, FeatureMapping_FeatureToMs2Indices & feature_ms2_indices)
        Preprocessing needed for SIRIUS
        
        Filter number of masstraces and perform feature mapping
        
        :param featureXML_path: Path to featureXML
        :param spectra: Input of MSExperiment with spectra information
        :param feature_mapping_info: Emtpy - stores FeatureMaps and KDTreeMaps internally
        :param feature_ms2_indices: Empty FeatureToMs2Indices
        """
        ...
    
    def logFeatureSpectraNumber(self, featureXML_path: Union[bytes, str, String] , feature_ms2_indices: FeatureMapping_FeatureToMs2Indices , spectra: MSExperiment ) -> None:
        """
        Cython signature: void logFeatureSpectraNumber(const String & featureXML_path, FeatureMapping_FeatureToMs2Indices & feature_ms2_indices, MSExperiment & spectra)
        Logs number of features and spectra used
        
        Prints the number of features and spectra used (OPENMS_LOG_INFO)
        
        :param featureXML_path: Path to featureXML
        :param feature_ms2_indices: FeatureToMs2Indices with feature mapping
        :param spectra: Input of MSExperiment with spectra information
        """
        ...
    
    def run(self, mzML_files: List[bytes] , featureXML_files: List[bytes] , out_ms: Union[bytes, str, String] , out_compoundinfo: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void run(const StringList & mzML_files, const StringList & featureXML_files, const String & out_ms, const String & out_compoundinfo)
        Runs SiriusExport with mzML and featureXML (optional) files as input.
        
        Generates a SIRIUS .ms file and compound info table (optional).
        
        :param mzML_files: List with paths to mzML files
        :param featureXML_files: List with paths to featureXML files
        :param out_ms: Output file name for SIRIUS .ms file
        :param out_compoundinfo: Output file name for tsv file with compound info
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


class SiriusMSFile:
    """
    Cython implementation of _SiriusMSFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SiriusMSFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SiriusMSFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: SiriusMSFile ) -> None:
        """
        Cython signature: void SiriusMSFile(SiriusMSFile &)
        """
        ... 


class SiriusMSFile_AccessionInfo:
    """
    Cython implementation of _SiriusMSFile_AccessionInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SiriusMSFile_AccessionInfo.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SiriusMSFile_AccessionInfo()
        """
        ...
    
    @overload
    def __init__(self, in_0: SiriusMSFile_AccessionInfo ) -> None:
        """
        Cython signature: void SiriusMSFile_AccessionInfo(SiriusMSFile_AccessionInfo &)
        """
        ... 


class SiriusMSFile_CompoundInfo:
    """
    Cython implementation of _SiriusMSFile_CompoundInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SiriusMSFile_CompoundInfo.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SiriusMSFile_CompoundInfo()
        """
        ...
    
    @overload
    def __init__(self, in_0: SiriusMSFile_CompoundInfo ) -> None:
        """
        Cython signature: void SiriusMSFile_CompoundInfo(SiriusMSFile_CompoundInfo &)
        """
        ... 


class SpectraMerger:
    """
    Cython implementation of _SpectraMerger

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectraMerger.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectraMerger()
        Merges blocks of MS or MS2 spectra
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectraMerger ) -> None:
        """
        Cython signature: void SpectraMerger(SpectraMerger &)
        """
        ...
    
    def mergeSpectraBlockWise(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void mergeSpectraBlockWise(MSExperiment & exp)
        """
        ...
    
    def mergeSpectraPrecursors(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void mergeSpectraPrecursors(MSExperiment & exp)
        Merges spectra with similar precursors (must have MS2 level)
        """
        ...
    
    def average(self, exp: MSExperiment , average_type: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void average(MSExperiment & exp, String average_type)
        Average over neighbouring spectra
        
        :param exp: Experimental data to be averaged
        :param average_type: Averaging type to be used ("gaussian" or "tophat")
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


class SqrtScaler:
    """
    Cython implementation of _SqrtScaler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SqrtScaler.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SqrtScaler()
        """
        ...
    
    @overload
    def __init__(self, in_0: SqrtScaler ) -> None:
        """
        Cython signature: void SqrtScaler(SqrtScaler &)
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


class StablePairFinder:
    """
    Cython implementation of _StablePairFinder

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1StablePairFinder.html>`_
      -- Inherits from ['BaseGroupFinder']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void StablePairFinder()
        """
        ...
    
    def run(self, input_maps: List[ConsensusMap] , result_map: ConsensusMap ) -> None:
        """
        Cython signature: void run(libcpp_vector[ConsensusMap] & input_maps, ConsensusMap & result_map)
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


class SwathWindowLoader:
    """
    Cython implementation of _SwathWindowLoader

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SwathWindowLoader.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SwathWindowLoader()
        """
        ...
    
    @overload
    def __init__(self, in_0: SwathWindowLoader ) -> None:
        """
        Cython signature: void SwathWindowLoader(SwathWindowLoader &)
        """
        ...
    
    def annotateSwathMapsFromFile(self, filename: Union[bytes, str, String] , swath_maps: List[SwathMap] , do_sort: bool , force: bool ) -> None:
        """
        Cython signature: void annotateSwathMapsFromFile(String filename, libcpp_vector[SwathMap] & swath_maps, bool do_sort, bool force)
        """
        ...
    
    def readSwathWindows(self, filename: Union[bytes, str, String] , swath_prec_lower: List[float] , swath_prec_upper: List[float] ) -> None:
        """
        Cython signature: void readSwathWindows(String filename, libcpp_vector[double] & swath_prec_lower, libcpp_vector[double] & swath_prec_upper)
        """
        ... 


class TMTTenPlexQuantitationMethod:
    """
    Cython implementation of _TMTTenPlexQuantitationMethod

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TMTTenPlexQuantitationMethod.html>`_
      -- Inherits from ['IsobaricQuantitationMethod']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TMTTenPlexQuantitationMethod()
        """
        ...
    
    @overload
    def __init__(self, in_0: TMTTenPlexQuantitationMethod ) -> None:
        """
        Cython signature: void TMTTenPlexQuantitationMethod(TMTTenPlexQuantitationMethod &)
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


class TransformationDescription:
    """
    Cython implementation of _TransformationDescription

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::TransformationDescription_1_1TransformationDescription.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TransformationDescription()
        """
        ...
    
    @overload
    def __init__(self, in_0: TransformationDescription ) -> None:
        """
        Cython signature: void TransformationDescription(TransformationDescription &)
        """
        ...
    
    def getDataPoints(self) -> List[TM_DataPoint]:
        """
        Cython signature: libcpp_vector[TM_DataPoint] getDataPoints()
        Returns the data points
        """
        ...
    
    @overload
    def setDataPoints(self, data: List[TM_DataPoint] ) -> None:
        """
        Cython signature: void setDataPoints(libcpp_vector[TM_DataPoint] & data)
        Sets the data points. Removes the model that was previously fitted to the data (if any)
        """
        ...
    
    @overload
    def setDataPoints(self, data: List[List[float, float]] ) -> None:
        """
        Cython signature: void setDataPoints(libcpp_vector[libcpp_pair[double,double]] & data)
        Sets the data points (backwards-compatible overload). Removes the model that was previously fitted to the data (if any)
        """
        ...
    
    def apply(self, in_0: float ) -> float:
        """
        Cython signature: double apply(double)
        Applies the transformation to `value`
        """
        ...
    
    @overload
    def fitModel(self, model_type: Union[bytes, str, String] , params: Param ) -> None:
        """
        Cython signature: void fitModel(String model_type, Param params)
        Fits a model to the data
        """
        ...
    
    @overload
    def fitModel(self, model_type: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void fitModel(String model_type)
        Fits a model to the data
        """
        ...
    
    def getModelType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getModelType()
        Gets the type of the fitted model
        """
        ...
    
    def getModelParameters(self) -> Param:
        """
        Cython signature: Param getModelParameters()
        Returns the model parameters
        """
        ...
    
    def invert(self) -> None:
        """
        Cython signature: void invert()
        Computes an (approximate) inverse of the transformation
        """
        ...
    
    def getDeviations(self, diffs: List[float] , do_apply: bool , do_sort: bool ) -> None:
        """
        Cython signature: void getDeviations(libcpp_vector[double] & diffs, bool do_apply, bool do_sort)
        Get the deviations between the data pairs
        
        :param diffs: Output
        :param do_apply: Get deviations after applying the model?
        :param do_sort: Sort `diffs` before returning?
        """
        ...
    
    def getStatistics(self) -> TransformationStatistics:
        """
        Cython signature: TransformationStatistics getStatistics()
        """
        ...
    
    getModelTypes: __static_TransformationDescription_getModelTypes 


class TransformationStatistics:
    """
    Cython implementation of _TransformationStatistics

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::TransformationDescription_1_1TransformationStatistics.html>`_
    """
    
    xmin: float
    
    xmax: float
    
    ymin: float
    
    ymax: float
    
    percentiles_before: Dict[int, float]
    
    percentiles_after: Dict[int, float]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TransformationStatistics()
        """
        ...
    
    @overload
    def __init__(self, in_0: TransformationStatistics ) -> None:
        """
        Cython signature: void TransformationStatistics(TransformationStatistics &)
        """
        ... 


class XMLHandler:
    """
    Cython implementation of _XMLHandler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1XMLHandler.html>`_
    """
    
    def __init__(self, filename: Union[bytes, str, String] , version: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void XMLHandler(const String & filename, const String & version)
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
    ActionMode : __ActionMode 


class XQuestResultXMLFile:
    """
    Cython implementation of _XQuestResultXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1XQuestResultXMLFile.html>`_
      -- Inherits from ['XMLFile']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void XQuestResultXMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: XQuestResultXMLFile ) -> None:
        """
        Cython signature: void XQuestResultXMLFile(XQuestResultXMLFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , pep_ids: List[PeptideIdentification] , prot_ids: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void load(const String & filename, libcpp_vector[PeptideIdentification] & pep_ids, libcpp_vector[ProteinIdentification] & prot_ids)
        Load the content of the xquest.xml file into the provided data structures
        
        :param filename: Filename of the file which is to be loaded
        :param pep_ids: Where the spectra with identifications of the input file will be loaded to
        :param prot_ids: Where the protein identification of the input file will be loaded to
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , poid: List[ProteinIdentification] , peid: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void store(const String & filename, libcpp_vector[ProteinIdentification] & poid, libcpp_vector[PeptideIdentification] & peid)
        Stores the identifications in a xQuest XML file
        """
        ...
    
    def getNumberOfHits(self) -> int:
        """
        Cython signature: int getNumberOfHits()
        Returns the total number of hits in the file
        """
        ...
    
    def getMinScore(self) -> float:
        """
        Cython signature: double getMinScore()
        Returns minimum score among the hits in the file
        """
        ...
    
    def getMaxScore(self) -> float:
        """
        Cython signature: double getMaxScore()
        Returns maximum score among the hits in the file
        """
        ...
    
    @overload
    def writeXQuestXMLSpec(self, out_file: Union[bytes, str, String] , base_name: Union[bytes, str, String] , preprocessed_pair_spectra: OPXL_PreprocessedPairSpectra , spectrum_pairs: List[List[int, int]] , all_top_csms: List[List[CrossLinkSpectrumMatch]] , spectra: MSExperiment , test_mode: bool ) -> None:
        """
        Cython signature: void writeXQuestXMLSpec(const String & out_file, const String & base_name, OPXL_PreprocessedPairSpectra preprocessed_pair_spectra, libcpp_vector[libcpp_pair[size_t,size_t]] spectrum_pairs, libcpp_vector[libcpp_vector[CrossLinkSpectrumMatch]] all_top_csms, MSExperiment spectra, const bool & test_mode)
        Writes spec.xml output containing matching peaks between heavy and light spectra after comparing and filtering
        
        :param out_file: Path and filename for the output file
        :param base_name: The base_name should be the name of the input spectra file without the file ending. Used as part of an identifier string for the spectra
        :param preprocessed_pair_spectra: The preprocessed spectra after comparing and filtering
        :param spectrum_pairs: Indices of spectrum pairs in the input map
        :param all_top_csms: CrossLinkSpectrumMatches, from which the IDs were generated. Only spectra with matches are written out
        :param spectra: The spectra, that were searched as a PeakMap. The indices in spectrum_pairs correspond to spectra in this map
        """
        ...
    
    @overload
    def writeXQuestXMLSpec(self, out_file: Union[bytes, str, String] , base_name: Union[bytes, str, String] , all_top_csms: List[List[CrossLinkSpectrumMatch]] , spectra: MSExperiment , test_mode: bool ) -> None:
        """
        Cython signature: void writeXQuestXMLSpec(const String & out_file, const String & base_name, libcpp_vector[libcpp_vector[CrossLinkSpectrumMatch]] all_top_csms, MSExperiment spectra, const bool & test_mode)
        Writes spec.xml output containing spectra for visualization. This version of the function is meant to be used for label-free linkers
        
        :param out_file: Path and filename for the output file
        :param base_name: The base_name should be the name of the input spectra file without the file ending. Used as part of an identifier string for the spectra
        :param all_top_csms: CrossLinkSpectrumMatches, from which the IDs were generated. Only spectra with matches are written out
        :param spectra: The spectra, that were searched as a PeakMap
        """
        ...
    
    def getVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getVersion()
        Return the version of the schema
        """
        ... 


class streampos:
    """
    Cython implementation of _streampos

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classstd_1_1streampos.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void streampos()
        """
        ...
    
    @overload
    def __init__(self, in_0: streampos ) -> None:
        """
        Cython signature: void streampos(streampos &)
        """
        ... 


class __ActionMode:
    None
    LOAD : int
    STORE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __CHARGEMODE_FD:
    None
    QFROMFEATURE : int
    QHEURISTIC : int
    QALL : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class DRangeIntersection:
    None
    Disjoint : int
    Intersects : int
    Inside : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class DecoyTransitionType:
    None
    UNKNOWN : int
    TARGET : int
    DECOY : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __NASFragmentType:
    None
    Full : int
    Internal : int
    FivePrime : int
    ThreePrime : int
    AIon : int
    BIon : int
    CIon : int
    XIon : int
    YIon : int
    ZIon : int
    Precursor : int
    BIonMinusH20 : int
    YIonMinusH20 : int
    BIonMinusNH3 : int
    YIonMinusNH3 : int
    NonIdentified : int
    Unannotated : int
    WIon : int
    AminusB : int
    DIon : int
    SizeOfNASFragmentType : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __PeakMassType:
    None
    MONOISOTOPIC : int
    AVERAGE : int
    SIZE_OF_PEAKMASSTYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class ScanMode:
    None
    UNKNOWN : int
    MASSSPECTRUM : int
    MS1SPECTRUM : int
    MSNSPECTRUM : int
    SIM : int
    SRM : int
    CRM : int
    CNG : int
    CNL : int
    PRECURSOR : int
    EMC : int
    TDF : int
    EMR : int
    EMISSION : int
    ABSORPTION : int
    SIZE_OF_SCANMODE : int

    def getMapping(self) -> Dict[int, str]:
       ... 

