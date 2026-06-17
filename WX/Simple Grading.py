import sys
def evaluate_grade(score):
    if score >= 80:          # คะแนนตั้งแต่ 80 ขึ้นไป (score >= 80) ส่งค่ากลับเป็น "Excellent"
        return "Excellent"
    
    elif score >= 50:            # คะแนนตั้งแต่ 50 ถึง 79 (50 <= score < 80) ส่งค่ากลับเป็น "Pass"
        return "Pass"
    
    else :                 # คะแนนต่ำกว่า 50 (score < 50) ส่งค่ากลับเป็น "Fail"
        return "Fail"

def main():
    test_score = 85
    result = evaluate_grade(test_score)
    print(f"Score: {test_score} -> Grade: {result}")

if __name__ == "__main__":
    main()
