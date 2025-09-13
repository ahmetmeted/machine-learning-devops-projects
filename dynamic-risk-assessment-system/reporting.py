import pandas as pd
import numpy as np
import json
import os
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def plot_confusion_matrix():
    """
    Function to generate confusion matrix plot
    """
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    test_data_path = config['test_data_path']
    output_model_path = config['output_model_path']
    
    # Import diagnostics functions
    from diagnostics import model_predictions
    
    # Read test data
    test_data_file = os.path.join(test_data_path, 'testdata.csv')
    if not os.path.exists(test_data_file):
        logger.error(f"Test data file not found at {test_data_file}")
        return
    
    df = pd.read_csv(test_data_file)
    
    # Get predictions
    predictions = model_predictions(df)
    actual = df['exited'].tolist()
    
    # Create confusion matrix
    cm = confusion_matrix(actual, predictions)
    
    # Create plot
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Not Exited', 'Exited'],
                yticklabels=['Not Exited', 'Exited'])
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    
    # Save plot
    os.makedirs(output_model_path, exist_ok=True)
    plot_path = os.path.join(output_model_path, 'confusionmatrix.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Confusion matrix saved to {plot_path}")
    
    return plot_path

def generate_pdf_report():
    """
    Function to generate PDF report
    """
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    output_model_path = config['output_model_path']
    output_folder_path = config['output_folder_path']
    prod_deployment_path = config['prod_deployment_path']
    
    # Import diagnostics functions
    from diagnostics import dataframe_summary, missing_data, execution_time, outdated_packages_list
    
    # Create PDF
    pdf_path = os.path.join(output_model_path, 'model_report.pdf')
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph("Dynamic Risk Assessment System - Model Report", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Date
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_para = Paragraph(f"Generated on: {date_str}", styles['Normal'])
    story.append(date_para)
    story.append(Spacer(1, 12))
    
    # Model Score
    score_file = os.path.join(prod_deployment_path, 'latestscore.txt')
    if os.path.exists(score_file):
        with open(score_file, 'r') as f:
            f1_score = f.read().strip()
        score_para = Paragraph(f"<b>Model F1 Score:</b> {f1_score}", styles['Normal'])
        story.append(score_para)
        story.append(Spacer(1, 12))
    
    # Ingested Files
    ingested_files_path = os.path.join(prod_deployment_path, 'ingestedfiles.txt')
    if os.path.exists(ingested_files_path):
        with open(ingested_files_path, 'r') as f:
            files = f.read().strip().split('\n')
        files_text = "Ingested Files: " + ", ".join(files)
        files_para = Paragraph(f"<b>{files_text}</b>", styles['Normal'])
        story.append(files_para)
        story.append(Spacer(1, 12))
    
    # Summary Statistics
    summary = dataframe_summary()
    if summary:
        story.append(Paragraph("<b>Summary Statistics:</b>", styles['Heading2']))
        for stat in summary:
            stat_text = f"{stat['column']}: Mean={stat['mean']:.2f}, Median={stat['median']:.2f}, Std={stat['std']:.2f}"
            stat_para = Paragraph(stat_text, styles['Normal'])
            story.append(stat_para)
        story.append(Spacer(1, 12))
    
    # Missing Data
    missing = missing_data()
    if missing:
        story.append(Paragraph("<b>Missing Data Percentages:</b>", styles['Heading2']))
        for i, pct in enumerate(missing):
            missing_text = f"Column {i}: {pct:.2f}% missing"
            missing_para = Paragraph(missing_text, styles['Normal'])
            story.append(missing_para)
        story.append(Spacer(1, 12))
    
    # Execution Times
    timing = execution_time()
    if timing:
        timing_text = f"Ingestion Time: {timing[0]:.2f} seconds, Training Time: {timing[1]:.2f} seconds"
        timing_para = Paragraph(f"<b>Execution Times:</b> {timing_text}", styles['Normal'])
        story.append(timing_para)
        story.append(Spacer(1, 12))
    
    # Package Versions
    packages = outdated_packages_list()
    if packages:
        story.append(Paragraph("<b>Package Versions:</b>", styles['Heading2']))
        for pkg in packages:
            pkg_text = f"{pkg['package']}: {pkg['current_version']} (Latest: {pkg['latest_version']})"
            pkg_para = Paragraph(pkg_text, styles['Normal'])
            story.append(pkg_para)
        story.append(Spacer(1, 12))
    
    # Add confusion matrix image
    confusion_matrix_path = os.path.join(output_model_path, 'confusionmatrix.png')
    if os.path.exists(confusion_matrix_path):
        story.append(Paragraph("<b>Confusion Matrix:</b>", styles['Heading2']))
        img = Image(confusion_matrix_path, width=6*inch, height=4.5*inch)
        story.append(img)
    
    # Build PDF
    doc.build(story)
    logger.info(f"PDF report saved to {pdf_path}")
    
    return pdf_path

if __name__ == '__main__':
    # Generate confusion matrix
    plot_confusion_matrix()
    
    # Generate PDF report
    generate_pdf_report()

