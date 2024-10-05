from flask import Flask, render_template, request
import math
from constants import (
    DEBUG_MODE, HOST, PORT,
    BMI_UNDERWEIGHT, BMI_NORMAL, BMI_OVERWEIGHT,
    BMI_CATEGORY_UNDERWEIGHT, BMI_CATEGORY_NORMAL, BMI_CATEGORY_OVERWEIGHT, BMI_CATEGORY_OBESE,
    GENDER_MALE,
    MALE_BMR_CONSTANT, MALE_BMR_WEIGHT_FACTOR, MALE_BMR_HEIGHT_FACTOR, MALE_BMR_AGE_FACTOR,
    FEMALE_BMR_CONSTANT, FEMALE_BMR_WEIGHT_FACTOR, FEMALE_BMR_HEIGHT_FACTOR, FEMALE_BMR_AGE_FACTOR,
    HEIGHT_CM_CONVERSION,
    ACTIVITY_FACTOR_SEDENTARY, ACTIVITY_FACTOR_LIGHTLY_ACTIVE, ACTIVITY_FACTOR_MODERATELY_ACTIVE,
    ACTIVITY_FACTOR_VERY_ACTIVE, ACTIVITY_FACTOR_EXTRA_ACTIVE,
    TEMPLATE_INDEX, TEMPLATE_RESULT
)

app = Flask(__name__)

def calculate_bmi(weight, height):
    """Calculate BMI given weight in kg and height in meters."""
    return weight / (height ** 2)

def classify_bmi(bmi):
    """Classify BMI into categories."""
    if bmi < BMI_UNDERWEIGHT:
        return BMI_CATEGORY_UNDERWEIGHT
    elif BMI_UNDERWEIGHT <= bmi < BMI_NORMAL:
        return BMI_CATEGORY_NORMAL
    elif BMI_NORMAL <= bmi < BMI_OVERWEIGHT:
        return BMI_CATEGORY_OVERWEIGHT
    else:
        return BMI_CATEGORY_OBESE

def calculate_daily_calories(weight, height, age, gender, activity_level):
    """Calculate daily calorie needs using the Harris-Benedict equation."""
    if gender.lower() == GENDER_MALE:
        bmr = MALE_BMR_CONSTANT + (MALE_BMR_WEIGHT_FACTOR * weight) + (MALE_BMR_HEIGHT_FACTOR * height * HEIGHT_CM_CONVERSION) - (MALE_BMR_AGE_FACTOR * age)
    else:
        bmr = FEMALE_BMR_CONSTANT + (FEMALE_BMR_WEIGHT_FACTOR * weight) + (FEMALE_BMR_HEIGHT_FACTOR * height * HEIGHT_CM_CONVERSION) - (FEMALE_BMR_AGE_FACTOR * age)
    
    activity_factors = {
        'sedentary': ACTIVITY_FACTOR_SEDENTARY,
        'lightly active': ACTIVITY_FACTOR_LIGHTLY_ACTIVE,
        'moderately active': ACTIVITY_FACTOR_MODERATELY_ACTIVE,
        'very active': ACTIVITY_FACTOR_VERY_ACTIVE,
        'extra active': ACTIVITY_FACTOR_EXTRA_ACTIVE
    }
    
    return bmr * activity_factors.get(activity_level.lower(), ACTIVITY_FACTOR_SEDENTARY)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        age = int(request.form['age'])
        gender = request.form['gender']
        activity_level = request.form['activity_level']

        bmi = calculate_bmi(weight, height)
        bmi_category = classify_bmi(bmi)
        daily_calories = calculate_daily_calories(weight, height, age, gender, activity_level)

        return render_template(TEMPLATE_RESULT, bmi=bmi, bmi_category=bmi_category, daily_calories=daily_calories)
    
    return render_template(TEMPLATE_INDEX)

if __name__ == "__main__":
    app.run(debug=DEBUG_MODE, host=HOST, port=PORT)

