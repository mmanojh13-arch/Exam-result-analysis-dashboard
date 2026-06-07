import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

class ExamAnalysis:
    """Class for analyzing exam results"""
    
    def __init__(self, csv_file):
        """Initialize with CSV file"""
        self.df = pd.read_csv(csv_file)
        self.results = {}
    
    def load_data(self):
        """Load and display data info"""
        print("\n" + "="*60)
        print("EXAM RESULT ANALYSIS DASHBOARD")
        print("="*60)
        print(f"\nTotal Students: {len(self.df)}")
        print(f"\nDataset Preview:")
        print(self.df.head(10))
        return self.df
    
    def basic_statistics(self):
        """Calculate basic statistics"""
        print("\n" + "="*60)
        print("BASIC STATISTICS")
        print("="*60)
        
        marks = self.df['marks']
        
        stats = {
            'Total Students': len(marks),
            'Average Score': round(marks.mean(), 2),
            'Median Score': round(marks.median(), 2),
            'Highest Score': marks.max(),
            'Lowest Score': marks.min(),
            'Standard Deviation': round(marks.std(), 2),
            'Range': marks.max() - marks.min()
        }
        
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        self.results['statistics'] = stats
        return stats
    
    def grade_distribution(self):
        """Assign grades and show distribution"""
        print("\n" + "="*60)
        print("GRADE DISTRIBUTION")
        print("="*60)
        
        def assign_grade(marks):
            if marks >= 90:
                return 'A'
            elif marks >= 80:
                return 'B'
            elif marks >= 70:
                return 'C'
            elif marks >= 60:
                return 'D'
            elif marks >= 40:
                return 'E'
            else:
                return 'F'
        
        self.df['Grade'] = self.df['marks'].apply(assign_grade)
        
        grade_dist = self.df['Grade'].value_counts().sort_index()
        
        print("\nGrade Distribution:")
        print(grade_dist)
        
        # Grade percentages
        print("\nGrade Percentages:")
        for grade, count in grade_dist.items():
            percentage = (count / len(self.df)) * 100
            print(f"  Grade {grade}: {count} students ({percentage:.1f}%)")
        
        self.results['grade_distribution'] = grade_dist.to_dict()
        return self.df
    
    def pass_fail_analysis(self):
        """Analyze pass/fail statistics (Pass >= 40)"""
        print("\n" + "="*60)
        print("PASS/FAIL ANALYSIS")
        print("="*60)
        
        pass_count = len(self.df[self.df['marks'] >= 40])
        fail_count = len(self.df[self.df['marks'] < 40])
        pass_percentage = (pass_count / len(self.df)) * 100
        fail_percentage = (fail_count / len(self.df)) * 100
        
        print(f"\nPassed (≥40): {pass_count} students ({pass_percentage:.1f}%)")
        print(f"Failed (<40): {fail_count} students ({fail_percentage:.1f}%)")
        
        self.results['pass_fail'] = {
            'passed': pass_count,
            'failed': fail_count,
            'pass_percentage': pass_percentage
        }
        
        return self.results['pass_fail']
    
    def top_performers(self, n=5):
        """Show top N performers"""
        print("\n" + "="*60)
        print(f"TOP {n} PERFORMERS")
        print("="*60)
        
        top_students = self.df.nlargest(n, 'marks')[['name', 'marks', 'Grade']]
        print("\n", top_students.to_string(index=False))
        
        return top_students
    
    def bottom_performers(self, n=5):
        """Show bottom N performers"""
        print("\n" + "="*60)
        print(f"BOTTOM {n} PERFORMERS")
        print("="*60)
        
        bottom_students = self.df.nsmallest(n, 'marks')[['name', 'marks', 'Grade']]
        print("\n", bottom_students.to_string(index=False))
        
        return bottom_students
    
    def subject_wise_analysis(self):
        """Analyze by subject if available"""
        if 'subject' not in self.df.columns:
            print("\nNo subject column found in data")
            return None
        
        print("\n" + "="*60)
        print("SUBJECT-WISE ANALYSIS")
        print("="*60)
        
        subject_stats = self.df.groupby('subject')['marks'].agg([
            ('Count', 'count'),
            ('Average', 'mean'),
            ('Highest', 'max'),
            ('Lowest', 'min'),
            ('Std Dev', 'std')
        ]).round(2)
        
        print("\n", subject_stats)
        
        return subject_stats
    
    def plot_score_distribution(self, filename='score_distribution.png'):
        """Plot histogram of score distribution"""
        plt.figure(figsize=(10, 6))
        plt.hist(self.df['marks'], bins=15, color='skyblue', edgecolor='black', alpha=0.7)
        plt.xlabel('Marks', fontsize=12)
        plt.ylabel('Number of Students', fontsize=12)
        plt.title('Score Distribution', fontsize=14, fontweight='bold')
        plt.grid(axis='y', alpha=0.3)
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\n✓ Score distribution plot saved as '{filename}'")
        plt.close()
    
    def plot_grade_distribution(self, filename='grade_distribution.png'):
        """Plot bar chart of grade distribution"""
        grade_counts = self.df['Grade'].value_counts().sort_index()
        plt.figure(figsize=(10, 6))
        colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#95a5a6', '#c0392b']
        bars = plt.bar(grade_counts.index, grade_counts.values, color=colors, edgecolor='black', alpha=0.8)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.xlabel('Grade', fontsize=12)
        plt.ylabel('Number of Students', fontsize=12)
        plt.title('Grade Distribution', fontsize=14, fontweight='bold')
        plt.grid(axis='y', alpha=0.3)
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Grade distribution plot saved as '{filename}'")
        plt.close()
    
    def plot_pass_fail(self, filename='pass_fail.png'):
        """Plot pie chart for pass/fail"""
        pass_count = len(self.df[self.df['marks'] >= 40])
        fail_count = len(self.df[self.df['marks'] < 40])
        
        plt.figure(figsize=(8, 6))
        colors = ['#2ecc71', '#e74c3c']
        plt.pie([pass_count, fail_count], labels=['Passed', 'Failed'], 
                autopct='%1.1f%%', colors=colors, startangle=90,
                textprops={'fontsize': 12, 'weight': 'bold'})
        plt.title('Pass/Fail Distribution', fontsize=14, fontweight='bold')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Pass/Fail pie chart saved as '{filename}'")
        plt.close()
    
    def plot_box_plot(self, filename='box_plot.png'):
        """Plot box plot for marks distribution"""
        plt.figure(figsize=(10, 6))
        box = plt.boxplot([self.df['marks']], labels=['Marks'], patch_artist=True)
        box['boxes'][0].set_facecolor('#3498db')
        plt.ylabel('Marks', fontsize=12)
        plt.title('Score Box Plot (Quartile Analysis)', fontsize=14, fontweight='bold')
        plt.grid(axis='y', alpha=0.3)
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Box plot saved as '{filename}'")
        plt.close()
    
    def generate_report(self, output_file='exam_report.txt'):
        """Generate complete text report"""
        with open(output_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("EXAM RESULT ANALYSIS REPORT\n")
            f.write("="*60 + "\n\n")
            
            # Basic Statistics
            f.write("BASIC STATISTICS\n")
            f.write("-"*60 + "\n")
            for key, value in self.results.get('statistics', {}).items():
                f.write(f"{key}: {value}\n")
            
            # Pass/Fail
            f.write("\n\nPASS/FAIL ANALYSIS\n")
            f.write("-"*60 + "\n")
            pf = self.results.get('pass_fail', {})
            f.write(f"Passed: {pf.get('passed', 0)} students ({pf.get('pass_percentage', 0):.1f}%)\n")
            f.write(f"Failed: {len(self.df) - pf.get('passed', 0)} students\n")
            
            # Grade Distribution
            f.write("\n\nGRADE DISTRIBUTION\n")
            f.write("-"*60 + "\n")
            for grade, count in sorted(self.results.get('grade_distribution', {}).items()):
                percentage = (count / len(self.df)) * 100
                f.write(f"Grade {grade}: {count} students ({percentage:.1f}%)\n")
            
            # Top 5 Performers
            f.write("\n\nTOP 5 PERFORMERS\n")
            f.write("-"*60 + "\n")
            top5 = self.df.nlargest(5, 'marks')[['name', 'marks', 'Grade']]
            for idx, row in top5.iterrows():
                f.write(f"{row['name']}: {row['marks']} ({row['Grade']})\n")
            
            # Bottom 5 Performers
            f.write("\n\nBOTTOM 5 PERFORMERS\n")
            f.write("-"*60 + "\n")
            bottom5 = self.df.nsmallest(5, 'marks')[['name', 'marks', 'Grade']]
            for idx, row in bottom5.iterrows():
                f.write(f"{row['name']}: {row['marks']} ({row['Grade']})\n")
        
        print(f"\n✓ Report saved as '{output_file}'")
    
    def full_analysis(self):
        """Run complete analysis and generate all outputs"""
        print("\n\n" + "🎯 "*20)
        print("STARTING COMPLETE EXAM ANALYSIS")
        print("🎯 "*20)
        
        self.load_data()
        self.basic_statistics()
        self.grade_distribution()
        self.pass_fail_analysis()
        self.top_performers()
        self.bottom_performers()
        self.subject_wise_analysis()
        
        # Generate visualizations
        print("\n" + "="*60)
        print("GENERATING VISUALIZATIONS")
        print("="*60)
        self.plot_score_distribution()
        self.plot_grade_distribution()
        self.plot_pass_fail()
        self.plot_box_plot()
        
        # Generate report
        self.generate_report()
        
        print("\n" + "✓ "*20)
        print("ANALYSIS COMPLETE!")
        print("✓ "*20)

