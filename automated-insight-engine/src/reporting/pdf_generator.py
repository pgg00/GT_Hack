from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from pathlib import Path
import logging
from datetime import datetime
from src.config import Config
import re

logger = logging.getLogger(__name__)

class PDFGenerator:
    """Generate premium, professional PDF reports using ReportLab"""
    
    # Professional color palette
    PRIMARY_COLOR = colors.HexColor('#1E40AF')      # Deep blue
    ACCENT_COLOR = colors.HexColor('#0EA5E9')       # Sky blue
    SUCCESS_COLOR = colors.HexColor('#10B981')      # Emerald
    WARNING_COLOR = colors.HexColor('#F59E0B')      # Amber
    DARK_BG = colors.HexColor('#0F172A')            # Navy
    LIGHT_BG = colors.HexColor('#F8FAFC')           # Off-white
    TEXT_DARK = colors.HexColor('#0F172A')
    TEXT_LIGHT = colors.HexColor('#64748B')
    BORDER_COLOR = colors.HexColor('#E2E8F0')
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Create premium custom paragraph styles"""
        
        # Section headers - premium style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=self.PRIMARY_COLOR,
            spaceAfter=16,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            borderPadding=0
        ))
        
        # Insight text
        self.styles.add(ParagraphStyle(
            name='InsightText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.TEXT_DARK,
            spaceAfter=10,
            alignment=TA_LEFT,
            fontName='Helvetica',
            leading=14
        ))
        
    def generate(self, data: dict, output_filename: str) -> Path:
        """Generate premium PDF report"""
        try:
            logger.info("📄 Generating premium PDF report...")
            
            output_path = Config.OUTPUT_DIR / output_filename
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=A4,
                rightMargin=0.5*inch,
                leftMargin=0.5*inch,
                topMargin=0.5*inch,
                bottomMargin=0.5*inch
            )
            
            story = []
            
            # ============ HEADER SECTION ============
            title_table = Table([['📊 Automated Data Analysis Report']], colWidths=[7.5*inch])
            title_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), self.PRIMARY_COLOR),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 24),
                ('TOPPADDING', (0, 0), (-1, -1), 20),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
                ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ]))
            story.append(title_table)
            
            # Subtitle with date
            date_str = datetime.now().strftime('%B %d, %Y at %I:%M %p')
            subtitle_table = Table([
                [f'Analysis of {data.get("title", "Campaign Data").replace("Analysis Report: ", "")} • Generated {date_str}']
            ], colWidths=[7.5*inch])
            subtitle_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), self.LIGHT_BG),
                ('TEXTCOLOR', (0, 0), (-1, -1), self.TEXT_LIGHT),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 20),
                ('BORDER', (0, 0), (-1, -1), 1, self.BORDER_COLOR),
            ]))
            story.append(subtitle_table)
            story.append(Spacer(1, 0.25*inch))
            
            # ============ KPI CARDS ============
            story.append(Paragraph("📈 Key Performance Indicators", self.styles['SectionHeader']))
            
            metrics = data.get('metrics', {})
            anomalies = data.get('anomalies', {})
            
            kpi_data = [
                [
                    '📊 Total Records',
                    '🚨 Anomalies',
                    '⚠️ Anomaly Rate'
                ],
                [
                    str(metrics.get('total_rows', 0)),
                    str(anomalies.get('anomaly_count', 0)),
                    f"{anomalies.get('anomaly_percentage', 0)}%"
                ]
            ]
            
            kpi_table = Table(kpi_data, colWidths=[2.3*inch, 2.3*inch, 2.3*inch])
            kpi_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.PRIMARY_COLOR),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, 1), self.LIGHT_BG),
                ('TEXTCOLOR', (0, 1), (-1, 1), self.PRIMARY_COLOR),
                ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 1), (-1, 1), 24),
                ('TOPPADDING', (0, 1), (-1, 1), 16),
                ('BOTTOMPADDING', (0, 1), (-1, 1), 16),
                ('GRID', (0, 0), (-1, -1), 1, self.BORDER_COLOR),
            ]))
            
            story.append(kpi_table)
            story.append(Spacer(1, 0.3*inch))
            
            # ============ AI INSIGHTS ============
            story.append(Paragraph("🤖 AI-Generated Executive Insights", self.styles['SectionHeader']))
            
            insights_text = data.get('insights', 'No insights available')
            
            # Sanitize and format insights
            insights_text = self._sanitize_html(insights_text)
            
            # Split into paragraphs for better layout
            paragraphs = insights_text.split('\n\n')
            insights_paras = []
            
            for para in paragraphs:
                if para.strip():
                    insights_paras.append(Paragraph(para.strip(), self.styles['InsightText']))
                    insights_paras.append(Spacer(1, 0.1*inch))
            
            # Container for insights
            insights_table = Table([[insights_paras]], colWidths=[6.8*inch])
            insights_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FEF3C7')),
                ('BORDER', (0, 0), (-1, -1), 2, self.WARNING_COLOR),
                ('TOPPADDING', (0, 0), (-1, -1), 16),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
                ('LEFTPADDING', (0, 0), (-1, -1), 16),
                ('RIGHTPADDING', (0, 0), (-1, -1), 16),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            story.append(insights_table)
            story.append(Spacer(1, 0.3*inch))
            
            # ============ STATISTICAL SUMMARY ============
            story.append(Paragraph("📊 Statistical Summary", self.styles['SectionHeader']))
            
            summary_stats = metrics.get('summary_stats', {})
            if summary_stats:
                stats_data = [['Metric', 'Mean', 'Median', 'Std Dev', 'Min', 'Max']]
                
                for col, stats in list(summary_stats.items())[:6]:
                    stats_data.append([
                        col,
                        f"{stats['mean']:,.0f}" if stats['mean'] > 100 else f"{stats['mean']:.2f}",
                        f"{stats['median']:,.0f}" if stats['median'] > 100 else f"{stats['median']:.2f}",
                        f"{stats['std']:,.0f}" if stats['std'] > 100 else f"{stats['std']:.2f}",
                        f"{stats['min']:,.0f}" if stats['min'] > 100 else f"{stats['min']:.2f}",
                        f"{stats['max']:,.0f}" if stats['max'] > 100 else f"{stats['max']:.2f}"
                    ])
                
                stats_table = Table(stats_data, colWidths=[1.2*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), self.PRIMARY_COLOR),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('TOPPADDING', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                    ('BACKGROUND', (0, 1), (-1, -1), self.LIGHT_BG),
                    ('TEXTCOLOR', (0, 1), (-1, -1), self.TEXT_DARK),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('TOPPADDING', (0, 1), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.LIGHT_BG]),
                    ('GRID', (0, 0), (-1, -1), 1, self.BORDER_COLOR),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, self.PRIMARY_COLOR),
                ]))
                
                story.append(stats_table)
            
            story.append(Spacer(1, 0.5*inch))
            
            # ============ FOOTER ============
            footer_table = Table([
                ['Generated by Automated Insight Engine | Powered by Gemini AI, Polars & Scikit-Learn']
            ], colWidths=[7.5*inch])
            footer_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), self.DARK_BG),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#94A3B8')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('TOPPADDING', (0, 0), (-1, -1), 15),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ]))
            story.append(footer_table)
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"✓ Premium PDF saved to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ PDF generation failed: {str(e)}")
            raise
    
    def _sanitize_html(self, text: str) -> str:
        """Sanitize and fix malformed HTML from AI output"""
        # Remove all HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Clean up markdown-style formatting
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
        text = text.replace('**', '')  # Remove stray asterisks
        
        # Normalize line breaks
        text = text.replace('\r\n', '\n')
        text = re.sub(r'\n{3,}', '\n\n', text)  # Max 2 consecutive newlines
        
        # Clean up bullets
        text = text.replace('•', '• ')
        text = text.replace('*', '• ')
        
        # Remove extra whitespace
        text = re.sub(r' +', ' ', text)
        text = text.strip()
        
        return text
