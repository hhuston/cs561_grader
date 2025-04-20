from canvasapi import Canvas
import pprint

API_URL = "https://sit.instructure.com/"

API_TOKEN = "1030~h4mGxDUAKFMWvMHF7ZwRBnncYGBarV2vXNyCTMG8UHt94HvLR2JFeveQcYEF6fCk"

canvas = Canvas(API_URL, API_TOKEN)

course = canvas.get_course(76619)

print(course)

pa2 = course.get_assignment(514026)
print(pa2)
submissions = pa2.get_submissions()
for submission in submissions:
    # pprint.pprint(submission.__dict__)
    file = submission.attachments[0]
    # file.download(".")
    print(file.get_contents())
    break

# test_student_submission.upload_comment(file="./api_test_comment")
# test_student_submission.edit(submission={"posted_grade": 100})