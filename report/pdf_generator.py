from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import os

class DigitalFootprintReport:
    def __init__(self, output_path="digital_footprint_report.pdf"):
        self.output_path = output_path
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Setup custom paragraph styles for the report."""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
        
    def generate_report(self, logins, file_shares, app_usage, user_info=None, date_range=None):
        """Generate the complete PDF report."""
        doc = SimpleDocTemplate(self.output_path, pagesize=A4)
        story = []
        
        # Title page
        story.extend(self.create_title_page(user_info))
        story.append(PageBreak())
        
        # Executive Summary
        story.extend(self.create_executive_summary(logins, file_shares, app_usage))
        story.append(PageBreak())
        
        # Detailed sections
        story.extend(self.create_login_section(logins))
        story.append(PageBreak())
        
        story.extend(self.create_file_shares_section(file_shares))
        story.append(PageBreak())
        
        story.extend(self.create_app_usage_section(app_usage))
        
        # Build PDF
        doc.build(story)
        return self.output_path
        
    def create_title_page(self, user_info):
        """Create the title page."""
        elements = []
        
        # Title
        title = Paragraph("Employee Digital Footprint Report", self.title_style)
        elements.append(title)
        elements.append(Spacer(1, 2*inch))
        
        # Report metadata
        if user_info:
            user_text = f"<b>Employee:</b> {user_info.get('name', 'Unknown')}"
            elements.append(Paragraph(user_text, self.normal_style))
        
        date_text = f"<b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        elements.append(Paragraph(date_text, self.normal_style))
        
        elements.append(Spacer(1, 3*inch))
        
        # Disclaimer
        disclaimer = Paragraph(
            "This report contains digital activity data collected from the user's system. "
            "Use this information responsibly and in compliance with applicable privacy laws and company policies.",
            self.normal_style
        )
        elements.append(disclaimer)
        
        return elements
        
    def create_executive_summary(self, logins, file_shares, app_usage):
        """Create the executive summary section."""
        elements = []
        
        # Section title
        title = Paragraph("Executive Summary", self.heading_style)
        elements.append(title)
        
        # Summary statistics
        summary_data = [
            ['Metric', 'Count', 'Details'],
            ['Login Events', str(len(logins)), f"From {len(set(l.get('source', '') for l in logins))} sources"],
            ['File Shares', str(len(file_shares)), f"Recent files and network drives"],
            ['Applications', str(len(app_usage)), f"Running processes and installed apps"],
            ['Report Period', 'N/A', f"Generated on {datetime.now().strftime('%Y-%m-%d')}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 1*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.5*inch))
        
        return elements
        
    def create_login_section(self, logins):
        """Create the login events section."""
        elements = []
        
        # Section title
        title = Paragraph("Login Events", self.heading_style)
        elements.append(title)
        
        if not logins:
            elements.append(Paragraph("No login events found.", self.normal_style))
            return elements
        
        # Login events table
        login_data = [['Timestamp', 'Username', 'Host', 'Type', 'Source']]
        
        for login in logins[:20]:  # Limit to 20 most recent
            login_data.append([
                login.get('timestamp', '').strftime('%Y-%m-%d %H:%M') if login.get('timestamp') else 'N/A',
                login.get('username', 'Unknown'),
                login.get('host', 'Unknown'),
                login.get('type', 'Unknown'),
                login.get('source', 'Unknown')
            ])
        
        login_table = Table(login_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1*inch, 1*inch])
        login_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8)
        ]))
        
        elements.append(login_table)
        
        if len(logins) > 20:
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph(f"Showing 20 of {len(logins)} login events.", self.normal_style))
        
        return elements
        
    def create_file_shares_section(self, file_shares):
        """Create the file shares section."""
        elements = []
        
        # Section title
        title = Paragraph("File Shares & Recent Files", self.heading_style)
        elements.append(title)
        
        if not file_shares:
            elements.append(Paragraph("No file shares or recent files found.", self.normal_style))
            return elements
        
        # File shares table
        file_data = [['Path', 'Type', 'Source', 'Last Accessed']]
        
        for file_share in file_shares[:20]:  # Limit to 20 most recent
            file_data.append([
                file_share.get('path', 'Unknown')[:50] + '...' if len(file_share.get('path', '')) > 50 else file_share.get('path', 'Unknown'),
                file_share.get('type', 'Unknown'),
                file_share.get('source', 'Unknown'),
                file_share.get('timestamp', '').strftime('%Y-%m-%d %H:%M') if file_share.get('timestamp') else 'N/A'
            ])
        
        file_table = Table(file_data, colWidths=[3*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        file_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8)
        ]))
        
        elements.append(file_table)
        
        if len(file_shares) > 20:
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph(f"Showing 20 of {len(file_shares)} file shares.", self.normal_style))
        
        return elements
        
    def create_app_usage_section(self, app_usage):
        """Create the application usage section."""
        elements = []
        
        # Section title
        title = Paragraph("Application Usage", self.heading_style)
        elements.append(title)
        
        if not app_usage:
            elements.append(Paragraph("No application usage data found.", self.normal_style))
            return elements
        
        # Separate running processes and installed apps
        running_processes = [app for app in app_usage if app.get('type') == 'running_process']
        installed_apps = [app for app in app_usage if app.get('type') == 'installed_app']
        
        # Running processes table
        if running_processes:
            elements.append(Paragraph("Currently Running Processes", self.normal_style))
            process_data = [['Name', 'PID', 'CPU %', 'Memory %', 'Start Time']]
            
            for process in running_processes[:15]:  # Limit to 15
                process_data.append([
                    process.get('name', 'Unknown')[:30] + '...' if len(process.get('name', '')) > 30 else process.get('name', 'Unknown'),
                    str(process.get('pid', 'N/A')),
                    f"{process.get('cpu_percent', 0):.1f}",
                    f"{process.get('memory_percent', 0):.1f}",
                    process.get('start_time', '').strftime('%H:%M') if process.get('start_time') else 'N/A'
                ])
            
            process_table = Table(process_data, colWidths=[2*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1.2*inch])
            process_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8)
            ]))
            
            elements.append(process_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Installed applications table
        if installed_apps:
            elements.append(Paragraph("Installed Applications", self.normal_style))
            app_data = [['Name', 'Install Date']]
            
            for app in installed_apps[:20]:  # Limit to 20
                app_data.append([
                    app.get('name', 'Unknown')[:50] + '...' if len(app.get('name', '')) > 50 else app.get('name', 'Unknown'),
                    app.get('install_date', 'N/A')
                ])
            
            app_table = Table(app_data, colWidths=[4*inch, 2*inch])
            app_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8)
            ]))
            
            elements.append(app_table)
        
        return elements 