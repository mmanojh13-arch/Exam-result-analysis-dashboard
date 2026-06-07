from analysis import ExamAnalysis
import os

def main():
    """Main function to run the exam analysis dashboard"""
    
    print("\n" + "="*70)
    print(" "*15 + "EXAM RESULT ANALYSIS DASHBOARD")
    print("="*70)
    
    # Check if CSV file exists
    csv_file = 'student_results.csv'
    
    if not os.path.exists(csv_file):
        print(f"\n❌ Error: '{csv_file}' not found!")
        print("\nPlease create a CSV file with the following format:")
        print("\nExample CSV content:")
        print("-" * 50)
        print("name,marks,subject")
        print("Raj Kumar,85,Mathematics")
        print("Priya Singh,92,English")
        print("Amit Patel,78,Science")
        print("-" * 50)
        return
    
    # Create analysis object and run analysis
    try:
        analysis = ExamAnalysis(csv_file)
        analysis.full_analysis()
        
        print("\n" + "="*70)
        print("FILES GENERATED:")
        print("="*70)
        print("  ✓ score_distribution.png  - Histogram of score distribution")
        print("  ✓ grade_distribution.png  - Bar chart of grades")
        print("  ✓ pass_fail.png          - Pie chart of pass/fail")
        print("  ✓ box_plot.png           - Box plot analysis")
        print("  ✓ exam_report.txt        - Text report")
        print("="*70)
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
