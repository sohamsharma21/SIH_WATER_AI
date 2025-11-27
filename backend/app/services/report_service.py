"""
PDF Report Generation Service using ReportLab
"""
import io
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import logging

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

from ..config import settings
from ..services.supabase_service import SupabaseService

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate PDF reports for wastewater treatment analysis."""
    
    def __init__(self):
        """Initialize report generator."""
        self.supabase_service = SupabaseService()
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#3b82f6'),
            spaceAfter=12
        ))
    
    def _create_cover_page(self, elements, plant_info: Optional[Dict[str, Any]] = None):
        """Create cover page."""
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph("SIH WATER AI", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph(
            "Industrial Wastewater Treatment Analysis Report",
            self.styles['Heading2']
        ))
        elements.append(Spacer(1, 1*inch))
        elements.append(Paragraph(
            f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['Normal']
        ))
        
        if plant_info:
            elements.append(Spacer(1, 0.3*inch))
            elements.append(Paragraph(
                f"Plant: {plant_info.get('name', 'Unknown')}",
                self.styles['Normal']
            ))
            elements.append(Paragraph(
                f"Location: {plant_info.get('location', 'Unknown')}",
                self.styles['Normal']
            ))
        
        elements.append(PageBreak())
    
    def _create_summary_page(self, elements, summary_data: Dict[str, Any]):
        """Create summary page."""
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Key metrics table
        data = [
            ['Metric', 'Value'],
            ['Quality Score', f"{summary_data.get('quality_score', 0):.2f}/100"],
            ['Contamination Index', f"{summary_data.get('contamination_index', 0):.2f}/100"],
            ['Expected Recovery', f"{summary_data.get('recovery_percentage', 0):.2f}%"],
            ['Reuse Type', summary_data.get('reuse_type', 'Unknown')]
        ]
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Recommendations
        if summary_data.get('recommendations'):
            elements.append(Paragraph("Key Recommendations", self.styles['SectionHeader']))
            for rec in summary_data['recommendations'][:5]:
                elements.append(Paragraph(f"• {rec}", self.styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
        
        elements.append(PageBreak())
    
    def _create_plant_diagram(self, elements):
        """Create plant diagram page (ASCII/text representation)."""
        elements.append(Paragraph("Treatment Plant Flow Diagram", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.3*inch))
        
        diagram_text = """
        PRIMARY TREATMENT → SECONDARY TREATMENT → TERTIARY TREATMENT → FINAL REUSE
        
        [Influent] → [Screening] → [Grit Removal] → [Primary Clarifier]
        ↓
        [Aeration Basin] → [Secondary Clarifier] → [Activated Sludge]
        ↓
        [Filtration] → [Disinfection] → [RO System*] → [Clean Water]
        ↓
        [Reuse/Discharge]
        
        *RO System: Activated only for drinking water quality
        """
        
        elements.append(Paragraph(diagram_text.replace('\n', '<br/>'), self.styles['Normal']))
        elements.append(PageBreak())
    
    def _create_sensor_table(self, elements, sensor_data: list):
        """Create sensor data table page."""
        elements.append(Paragraph("Raw Sensor Data", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.3*inch))
        
        if not sensor_data:
            elements.append(Paragraph("No sensor data available.", self.styles['Normal']))
            elements.append(PageBreak())
            return
        
        # Limit to recent 50 readings for table
        sensor_data = sensor_data[:50]
        
        # Prepare table data
        headers = ['Timestamp', 'Sensor ID', 'Parameter', 'Value', 'Unit']
        table_data = [headers]
        
        for sensor in sensor_data:
            table_data.append([
                sensor.get('timestamp', 'N/A')[:19] if sensor.get('timestamp') else 'N/A',
                sensor.get('sensor_id', 'N/A'),
                sensor.get('parameter_name', 'N/A'),
                f"{sensor.get('value', 0):.2f}",
                sensor.get('unit', 'N/A')
            ])
        
        table = Table(table_data, colWidths=[1.5*inch, 1*inch, 1.2*inch, 1*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(table)
        elements.append(PageBreak())
    
    def _create_prediction_page(self, elements, prediction_data: Dict[str, Any]):
        """Create prediction results page."""
        elements.append(Paragraph("ML Model Predictions", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.3*inch))
        
        pred_info = [
            ['Model Name', prediction_data.get('model_name', 'Unknown')],
            ['Quality Score', f"{prediction_data.get('quality_score', 0):.2f}/100"],
            ['Contamination Index', f"{prediction_data.get('contamination_index', 0):.2f}/100"],
            ['Confidence', f"{prediction_data.get('confidence', 0)*100:.2f}%"]
        ]
        
        table = Table(pred_info, colWidths=[2.5*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightblue)
        ]))
        
        elements.append(table)
        elements.append(PageBreak())
    
    def _create_treatment_flow_page(self, elements, optimization_results: Dict[str, Any]):
        """Create treatment flow recommendations page."""
        elements.append(Paragraph("Recommended Treatment Flow", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Primary Treatment
        primary = optimization_results.get('primary_treatment', {})
        elements.append(Paragraph("Primary Treatment", self.styles['Heading3']))
        primary_data = [
            ['Parameter', 'Value'],
            ['Settling Time', f"{primary.get('settling_time_min', 0):.1f} minutes"],
            ['Coagulant Dose', f"{primary.get('coagulant_dose_ml', 0):.2f} mL"],
            ['Sludge Volume Index', f"{primary.get('sludge_volume_index', 0):.2f} mL/g"]
        ]
        table = Table(primary_data, colWidths=[2.5*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Secondary Treatment
        secondary = optimization_results.get('secondary_treatment', {})
        elements.append(Paragraph("Secondary Treatment", self.styles['Heading3']))
        secondary_data = [
            ['Parameter', 'Value'],
            ['Aeration Time', f"{secondary.get('aeration_time_min', 0):.1f} minutes"],
            ['DO Target', f"{secondary.get('do_target_ppm', 0):.2f} ppm"],
            ['Blower Speed', f"{secondary.get('blower_speed_rpm', 0):.0f} RPM"],
            ['Sludge Age', f"{secondary.get('sludge_age_days', 0):.1f} days"]
        ]
        table = Table(secondary_data, colWidths=[2.5*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Tertiary Treatment
        tertiary = optimization_results.get('tertiary_treatment', {})
        elements.append(Paragraph("Tertiary Treatment", self.styles['Heading3']))
        tertiary_data = [
            ['Parameter', 'Value'],
            ['Filtration Rate', f"{tertiary.get('filtration_rate_lpm', 0):.2f} LPM/m²"],
            ['Chlorine Dose', f"{tertiary.get('chlorine_dose_ml', 0):.2f} mL"],
            ['RO Required', 'Yes' if tertiary.get('ro_trigger') else 'No']
        ]
        table = Table(tertiary_data, colWidths=[2.5*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f59e0b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(PageBreak())
    
    def _create_graphs_page(self, elements):
        """Create graphs page (placeholder for charts)."""
        elements.append(Paragraph("Data Visualizations", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph(
            "Time-series charts and visualizations would be included here.",
            self.styles['Normal']
        ))
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph(
            "This section can be extended to include matplotlib/plotly generated charts.",
            self.styles['Normal']
        ))
        elements.append(PageBreak())
    
    def generate_report(
        self,
        prediction_data: Dict[str, Any],
        optimization_results: Dict[str, Any],
        sensor_data: Optional[list] = None,
        plant_info: Optional[Dict[str, Any]] = None
    ) -> bytes:
        """
        Generate complete PDF report.
        
        Returns:
            PDF file as bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Cover page
        self._create_cover_page(elements, plant_info)
        
        # Summary
        summary = {
            'quality_score': prediction_data.get('quality_score', 0),
            'contamination_index': prediction_data.get('contamination_index', 0),
            'recovery_percentage': optimization_results.get('expected_recovery_percentage', 0),
            'reuse_type': optimization_results.get('final_reuse', {}).get('reuse_type', 'Unknown'),
            'recommendations': optimization_results.get('recommended_process_steps', [])
        }
        self._create_summary_page(elements, summary)
        
        # Plant diagram
        self._create_plant_diagram(elements)
        
        # Sensor data
        self._create_sensor_table(elements, sensor_data or [])
        
        # Predictions
        self._create_prediction_page(elements, prediction_data)
        
        # Treatment flow
        self._create_treatment_flow_page(elements, optimization_results)
        
        # Graphs
        self._create_graphs_page(elements)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return buffer.read()
    
    def save_and_upload_report(
        self,
        pdf_bytes: bytes,
        report_name: Optional[str] = None
    ) -> Optional[str]:
        """
        Save PDF and upload to Supabase Storage.
        
        Returns:
            Public URL of uploaded report
        """
        if report_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"report_{timestamp}.pdf"
        
        try:
            # Upload to Supabase Storage
            public_url = self.supabase_service.upload_file_to_storage(
                bucket=settings.REPORTS_BUCKET,
                file_path=report_name,
                file_content=pdf_bytes
            )
            
            if public_url:
                # Ensure URL is a string
                if isinstance(public_url, dict):
                    public_url = public_url.get('publicUrl') or public_url.get('url')
                
                # Save metadata
                report_metadata = {
                    'report_name': report_name,
                    'report_type': 'treatment_analysis',
                    'storage_path': report_name,
                    'public_url': str(public_url) if public_url else report_name,
                    'file_size': len(pdf_bytes),
                    'generated_at': datetime.now().isoformat()
                }
                self.supabase_service.insert_report_metadata(report_metadata)
            
            return public_url if public_url else report_name
        except Exception as e:
            logger.error(f"Error uploading report: {str(e)}", exc_info=True)
            return None

