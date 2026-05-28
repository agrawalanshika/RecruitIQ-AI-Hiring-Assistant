def rank_candidates(candidate_results):

    ranked_candidates = sorted(

        candidate_results,

        key=lambda x: x["match_result"]["final_score"],

        reverse=True

    )

    return ranked_candidates