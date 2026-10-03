from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def knapsack(subjects, max_credits):
    n = len(subjects)

    dp = [[0] * (max_credits + 1) for _ in range(n + 1)]

    # Dynamic Programming
    for i in range(1, n + 1):
        credits = subjects[i - 1]["credits"]
        score = subjects[i - 1]["score"]

        for c in range(max_credits + 1):

            if credits <= c:
                dp[i][c] = max(
                    dp[i - 1][c],
                    score + dp[i - 1][c - credits]
                )
            else:
                dp[i][c] = dp[i - 1][c]

    # Find selected subjects
    selected = []
    c = max_credits

    for i in range(n, 0, -1):

        if dp[i][c] != dp[i - 1][c]:
            selected.append(subjects[i - 1])
            c -= subjects[i - 1]["credits"]

    selected.reverse()

    return selected, dp[n][max_credits]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/select", methods=["POST"])
def select_subjects():

    data = request.json

    subjects = data["subjects"]
    max_credits = int(data["max_credits"])

    selected, score = knapsack(subjects, max_credits)

    total_credits = sum(subject["credits"] for subject in selected)

    return jsonify({
        "selected": selected,
        "total_credits": total_credits,
        "score": score
    })


if __name__ == "__main__":
    app.run(debug=True)