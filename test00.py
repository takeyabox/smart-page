import os

quiz = """
{
  "title": "物質の状態に関する理解度テスト",
  "questions": [
    {
      "id": 1,
      "question_text": "物質の三態とはどのような状態を指しているか？",
      "options": [
        "固体、液体、気体",
        "固体、液体、プラズマ",
        "液体、気体、エネルギー",
        "固体、液体、ガス"
      ],
      "correct_answer": "固体、液体、気体",
      "explanation": "物質の三態とは、固体、液体、気体の3つの状態のことであり、物質はこれらの状態に応じてその粒子のふるまいが異なる。"
    },
    {
      "id": 2,
      "question_text": "融解とはどのような現象を指すか？",
      "options": [
        "固体が冷却されて固体になること",
        "液体が気体になること",
        "固体が加熱されて液体になること",
        "気体が液体になること"
      ],
      "correct_answer": "固体が加熱されて液体になること",
      "explanation": "融解とは、一定の圧力のもとで固体を加熱すると、ある温度で固体から液体に変化する現象を指す。"
    },
    {
      "id": 3,
      "question_text": "水の融解熱はどのくらいか？",
      "options": [
        "6.01 kJ/mol",
        "40.7 kJ/mol",
        "5.00 kJ/mol",
        "10.2 kJ/mol"
      ],
      "correct_answer": "6.01 kJ/mol",
      "explanation": "水（氷）の融解熱は6.01 kJ/molであり、これは1 molの固体が融解する際に吸収される熱エネルギーの量を示している。"
    }
  ]
}"""

checkStringArray = ["{" ,"title", "questions", "id", "question_text", "options", "correct_answer", "explanation", "}"]
for checkstring in checkStringArray:
    checkerrors = quiz.find(checkstring)
    if checkerrors == -1:
        print(f"Error: {checkstring} not found")


api_key = os.environ.get("CHATGPT_API_KEY")
if api_key is None:
    print("Error: CHATGPT_API_KEY environment variable not set")
else:
    print (f"your api key is <{api_key[:5]}.....>")

delete_before = quiz.find("{")
delete_after = quiz.rfind("}") + 1
quiz = quiz[delete_before:delete_after]
print(quiz)