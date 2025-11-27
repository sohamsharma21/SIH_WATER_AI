"""
Treatment Optimization Engine
AI-driven optimization for Primary, Secondary, and Tertiary treatment stages
"""
import numpy as np
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PrimaryTreatmentOptimizer:
    """Optimizer for Primary Treatment stage."""
    
    @staticmethod
    def optimize(quality_score: float, contamination_index: float, 
                 flow_rate_lpm: float = 1000.0, **kwargs) -> Dict[str, Any]:
        """
        Optimize primary treatment parameters.
        
        Args:
            quality_score: Water quality score (0-100)
            contamination_index: Contamination level (0-100)
            flow_rate_lpm: Flow rate in liters per minute
            
        Returns:
            Optimization recommendations
        """
        # Calculate settling time based on contamination
        # Higher contamination = longer settling time
        base_settling_time = 60  # minutes
        contamination_factor = contamination_index / 100.0
        settling_time = base_settling_time * (1 + contamination_factor * 2)
        settling_time = max(30, min(settling_time, 180))  # Clamp between 30-180 min
        
        # Coagulant dosing (Aluminum sulfate or ferric chloride)
        # Higher contamination = more coagulant
        base_dose = 50  # mg/L
        dose_multiplier = 1 + (contamination_index / 100.0) * 1.5
        coagulant_dose_ml = (base_dose * dose_multiplier * flow_rate_lpm) / 1000
        coagulant_dose_ml = max(20, min(coagulant_dose_ml, 200))  # Clamp
        
        # Sludge Volume Index (SVI) - target range 50-150 mL/g
        # Higher contamination = higher SVI expected
        svi = 80 + (contamination_index / 100.0) * 50
        svi = max(50, min(svi, 200))
        
        return {
            'settling_time_min': round(settling_time, 2),
            'coagulant_dose_ml': round(coagulant_dose_ml, 2),
            'sludge_volume_index': round(svi, 2),
            'recommendations': [
                f"Maintain settling time of {settling_time:.0f} minutes",
                f"Apply coagulant dose of {coagulant_dose_ml:.1f} mL",
                f"Monitor SVI - target: {svi:.0f} mL/g"
            ]
        }


class SecondaryTreatmentOptimizer:
    """Optimizer for Secondary Treatment (Biological Treatment)."""
    
    @staticmethod
    def optimize(quality_score: float, contamination_index: float,
                 current_bod: float = 200.0, current_cod: float = 400.0,
                 **kwargs) -> Dict[str, Any]:
        """
        Optimize secondary treatment parameters.
        
        Args:
            quality_score: Water quality score (0-100)
            contamination_index: Contamination level (0-100)
            current_bod: Current BOD level (mg/L)
            current_cod: Current COD level (mg/L)
            
        Returns:
            Optimization recommendations
        """
        # Aeration time calculation
        # Higher BOD/COD = longer aeration needed
        bod_target = 30  # Target BOD after treatment
        cod_target = 100  # Target COD after treatment
        
        bod_reduction_needed = max(0, current_bod - bod_target)
        cod_reduction_needed = max(0, current_cod - cod_target)
        
        # Base aeration: 4-8 hours depending on load
        base_aeration_time = 240  # minutes
        aeration_factor = (bod_reduction_needed / 200.0) + (cod_reduction_needed / 400.0)
        aeration_time = base_aeration_time * (1 + aeration_factor)
        aeration_time = max(180, min(aeration_time, 480))  # 3-8 hours
        
        # Dissolved Oxygen (DO) target
        # Optimal range: 2-4 mg/L
        do_target = 2.5 + (contamination_index / 100.0) * 1.0
        do_target = max(2.0, min(do_target, 4.0))
        
        # Blower speed control (ML-driven)
        # Higher contamination = higher blower speed
        base_blower_speed = 1000  # RPM
        blower_factor = 1 + (contamination_index / 100.0) * 0.5
        blower_speed = base_blower_speed * blower_factor
        blower_speed = max(800, min(blower_speed, 1500))
        
        # Sludge age (Mean Cell Residence Time)
        # Optimal: 5-15 days
        sludge_age = 8 + (contamination_index / 100.0) * 5
        sludge_age = max(5, min(sludge_age, 15))
        
        return {
            'aeration_time_min': round(aeration_time, 2),
            'do_target_ppm': round(do_target, 2),
            'blower_speed_rpm': round(blower_speed, 0),
            'sludge_age_days': round(sludge_age, 2),
            'recommendations': [
                f"Aerate for {aeration_time:.0f} minutes",
                f"Maintain DO at {do_target:.2f} mg/L",
                f"Set blower speed to {blower_speed:.0f} RPM",
                f"Target sludge age: {sludge_age:.1f} days"
            ]
        }


class TertiaryTreatmentOptimizer:
    """Optimizer for Tertiary Treatment (Polishing)."""
    
    @staticmethod
    def optimize(quality_score: float, contamination_index: float,
                 target_quality: str = "environmental", **kwargs) -> Dict[str, Any]:
        """
        Optimize tertiary treatment parameters.
        
        Args:
            quality_score: Water quality score (0-100)
            contamination_index: Contamination level (0-100)
            target_quality: Target quality ("environmental", "industrial", "irrigation", "drinking")
            
        Returns:
            Optimization recommendations
        """
        # Filtration rate
        # Higher quality needed = slower filtration
        base_filtration_rate = 10  # LPM per m²
        quality_factor = (100 - quality_score) / 100.0
        filtration_rate = base_filtration_rate * (1 - quality_factor * 0.3)
        filtration_rate = max(5, min(filtration_rate, 15))
        
        # Chlorine dosing for disinfection
        # Higher contamination = more chlorine
        base_chlorine_dose = 2  # mg/L
        chlorine_multiplier = 1 + (contamination_index / 100.0) * 1.0
        chlorine_dose_ml = base_chlorine_dose * chlorine_multiplier
        chlorine_dose_ml = max(1, min(chlorine_dose_ml, 5))  # Safe range
        
        # Reverse Osmosis (RO) trigger
        # Required for drinking water or high contamination
        ro_required = (
            target_quality == "drinking" or
            contamination_index > 70 or
            quality_score < 50
        )
        
        return {
            'filtration_rate_lpm': round(filtration_rate, 2),
            'chlorine_dose_ml': round(chlorine_dose_ml, 2),
            'ro_trigger': ro_required,
            'recommendations': [
                f"Set filtration rate to {filtration_rate:.1f} LPM/m²",
                f"Apply chlorine dose of {chlorine_dose_ml:.2f} mg/L",
                "RO required" if ro_required else "RO not required"
            ]
        }


class FinalReuseEngine:
    """Determines final reuse suitability and recovery percentage."""
    
    @staticmethod
    def determine_reuse(quality_score: float, contamination_index: float,
                       ro_used: bool = False, **kwargs) -> Dict[str, Any]:
        """
        Determine suitable reuse type and recovery percentage.
        
        Args:
            quality_score: Water quality score (0-100)
            contamination_index: Contamination level (0-100)
            ro_used: Whether Reverse Osmosis was applied
            
        Returns:
            Reuse recommendations
        """
        # Determine reuse type based on quality
        if ro_used and quality_score >= 95:
            reuse_type = "drinking"
            recovery_percentage = 75  # RO has lower recovery
            description = "Suitable for drinking water after RO treatment"
        
        elif quality_score >= 85 and contamination_index < 20:
            reuse_type = "industrial"
            recovery_percentage = 90
            description = "Suitable for industrial reuse (cooling, process water)"
        
        elif quality_score >= 70 and contamination_index < 40:
            reuse_type = "irrigation"
            recovery_percentage = 85
            description = "Suitable for agricultural irrigation"
        
        elif quality_score >= 60 and contamination_index < 60:
            reuse_type = "environmental"
            recovery_percentage = 95
            description = "Suitable for environmental discharge"
        
        else:
            reuse_type = "environmental"
            recovery_percentage = 90
            description = "Requires further treatment before reuse"
        
        return {
            'reuse_type': reuse_type,
            'recovery_percentage': recovery_percentage,
            'description': description,
            'quality_score': round(quality_score, 2),
            'contamination_index': round(contamination_index, 2)
        }


class TreatmentOptimizerEngine:
    """Main treatment optimization engine that combines all stages."""
    
    def __init__(self):
        """Initialize optimizer engine."""
        self.primary_optimizer = PrimaryTreatmentOptimizer()
        self.secondary_optimizer = SecondaryTreatmentOptimizer()
        self.tertiary_optimizer = TertiaryTreatmentOptimizer()
        self.reuse_engine = FinalReuseEngine()
    
    def optimize_all(
        self,
        quality_score: float,
        contamination_index: float,
        sensor_data: Optional[Dict[str, float]] = None,
        target_quality: str = "environmental"
    ) -> Dict[str, Any]:
        """
        Optimize all treatment stages.
        
        Args:
            quality_score: Predicted quality score (0-100)
            contamination_index: Predicted contamination index (0-100)
            sensor_data: Optional sensor readings (BOD, COD, flow rate, etc.)
            target_quality: Target quality level
            
        Returns:
            Complete optimization results
        """
        sensor_data = sensor_data or {}
        
        # Extract sensor values
        flow_rate = sensor_data.get('flow_rate_lpm', 1000.0)
        current_bod = sensor_data.get('bod', 200.0)
        current_cod = sensor_data.get('cod', 400.0)
        
        # Primary treatment
        primary_results = self.primary_optimizer.optimize(
            quality_score=quality_score,
            contamination_index=contamination_index,
            flow_rate_lpm=flow_rate
        )
        
        # Secondary treatment
        secondary_results = self.secondary_optimizer.optimize(
            quality_score=quality_score,
            contamination_index=contamination_index,
            current_bod=current_bod,
            current_cod=current_cod
        )
        
        # Tertiary treatment
        tertiary_results = self.tertiary_optimizer.optimize(
            quality_score=quality_score,
            contamination_index=contamination_index,
            target_quality=target_quality
        )
        
        # Final reuse determination
        reuse_results = self.reuse_engine.determine_reuse(
            quality_score=quality_score,
            contamination_index=contamination_index,
            ro_used=tertiary_results.get('ro_trigger', False)
        )
        
        # Combine all results
        return {
            'quality_score': round(quality_score, 2),
            'contamination_index': round(contamination_index, 2),
            'primary_treatment': primary_results,
            'secondary_treatment': secondary_results,
            'tertiary_treatment': tertiary_results,
            'final_reuse': reuse_results,
            'dosing_ml': {
                'coagulant': primary_results['coagulant_dose_ml'],
                'chlorine': tertiary_results['chlorine_dose_ml']
            },
            'recommended_process_steps': [
                *primary_results['recommendations'],
                *secondary_results['recommendations'],
                *tertiary_results['recommendations']
            ],
            'expected_recovery_percentage': reuse_results['recovery_percentage']
        }

