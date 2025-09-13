#!/usr/bin/env python3
"""
Training script for the Census Income Prediction Model
"""

import os
from model import train_model


def main():
    """Main training function."""
    print("Starting model training...")

    # Create model directory
    os.makedirs('model', exist_ok=True)

    # Train the model
    model, df = train_model()

    # Calculate slice performance
    print("\nCalculating slice performance...")
    slice_performance = model.get_slice_performance(df, 'education')

    # Save slice performance to file
    with open('slice_output.txt', 'w') as f:
        f.write("Model Performance on Education Slices\n")
        f.write("=" * 50 + "\n\n")

        for education, metrics in slice_performance.items():
            f.write(f"Education: {education}\n")
            f.write(f"  Count: {metrics['count']}\n")
            f.write(f"  Accuracy: {metrics['accuracy']:.4f}\n")
            f.write(f"  Precision: {metrics['precision']:.4f}\n")
            f.write(f"  Recall: {metrics['recall']:.4f}\n")
            f.write(f"  F1-Score: {metrics['f1']:.4f}\n")
            f.write("\n")

    print("Slice performance saved to slice_output.txt")
    print("Training completed successfully!")


if __name__ == "__main__":
    main()
