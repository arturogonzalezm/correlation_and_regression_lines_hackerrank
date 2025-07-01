from correlation import CorrelationContext, PearsonCorrelationStrategy

if __name__ == "__main__":
    physics_scores = [15, 12, 8, 8, 7, 7, 7, 6, 5, 3]
    history_scores = [10, 25, 17, 11, 13, 17, 20, 13, 9, 15]

    ctx = CorrelationContext(PearsonCorrelationStrategy())
    r = ctx.execute(physics_scores, history_scores)
    # print only the coefficient rounded to three decimal places
    print(f"{r:.3f}")
