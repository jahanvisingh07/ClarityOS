import unittest
from unittest.mock import patch

from fastapi import HTTPException

import main
from quiz_scoring import CAREER_SIGNALS, CAREER_TRACKS, score_careers


class QuizScoringTests(unittest.TestCase):
    def test_every_supported_track_ranks_its_matching_interest(self):
        for stream, careers in CAREER_TRACKS.items():
            with self.subTest(stream=stream):
                expected_title, signal_group = next(iter(careers.items()))
                matching_interest = CAREER_SIGNALS[signal_group][0]
                answers = {question_id: "I am not sure yet" for question_id in range(1, 21)}
                answers[20] = f"I would like to explore {matching_interest}"

                ranked = score_careers(stream, answers)

                self.assertEqual(ranked[0]["title"], expected_title)
                self.assertEqual({match["title"] for match in ranked}, set(careers))
                self.assertTrue(all(0 <= match["match"] <= 100 for match in ranked))

    def test_answers_from_each_question_can_change_alignment(self):
        answers = {question_id: "I am not sure yet" for question_id in range(1, 21)}
        baseline = score_careers("College - Computer Science & IT", answers)
        baseline_score = next(
            match["match"]
            for match in baseline
            if match["title"] == "Full-Stack / Core Software Engineering"
        )

        for question_id in range(1, 21):
            with self.subTest(question_id=question_id):
                changed_answers = dict(answers)
                changed_answers[question_id] = "I enjoy coding and building software"
                ranked = score_careers("College - Computer Science & IT", changed_answers)
                changed_score = next(
                    match["match"]
                    for match in ranked
                    if match["title"] == "Full-Stack / Core Software Engineering"
                )
                self.assertGreater(changed_score, baseline_score)

    def test_negative_interest_does_not_increase_a_career_score(self):
        answers = {question_id: "I am not sure yet" for question_id in range(1, 21)}
        answers[5] = "I do not like coding"

        ranked = score_careers("College - Computer Science & IT", answers)

        software_score = next(
            match["match"]
            for match in ranked
            if match["title"] == "Full-Stack / Core Software Engineering"
        )
        self.assertEqual(software_score, 0)

    def test_no_matching_signals_does_not_create_a_recommendation(self):
        answers = {question_id: "I am not sure yet" for question_id in range(1, 21)}

        with patch.object(main.model, "generate_content") as generate_content:
            result = self.run_endpoint("Science (PCB)", answers)

        self.assertIsNone(result["optimal_vector"])
        self.assertIn("do not yet point strongly", result["explanation"])
        generate_content.assert_not_called()

    def test_incomplete_answers_are_rejected(self):
        with self.assertRaises(HTTPException) as error:
            self.run_endpoint("Science (PCB)", {1: "Biology"})

        self.assertEqual(error.exception.status_code, 422)

    def test_json_string_question_ids_are_accepted(self):
        answers = {str(question_id): "I am not sure yet" for question_id in range(1, 21)}
        answers["20"] = "I would like to explore doctor"

        with patch.object(main.model, "generate_content") as generate_content:
            generate_content.return_value.text = "Try learning more about healthcare."
            result = self.run_endpoint("Science (PCB)", answers)

        self.assertEqual(result["optimal_vector"]["title"], "Medicine (MBBS/BDS)")

    def test_unknown_tracks_are_rejected(self):
        answers = {question_id: "I am not sure yet" for question_id in range(1, 21)}

        with self.assertRaises(HTTPException) as error:
            self.run_endpoint("Unknown stream", answers)

        self.assertEqual(error.exception.status_code, 422)

    def test_explanation_service_failure_still_returns_scored_results(self):
        answers = {question_id: "I am not sure yet" for question_id in range(1, 21)}
        answers[1] = "I enjoy coding"

        with patch.object(main.model, "generate_content", side_effect=RuntimeError("offline")):
            with self.assertLogs(main.logger, level="ERROR"):
                result = self.run_endpoint("College - Computer Science & IT", answers)

        self.assertEqual(result["status"], "success")
        self.assertIsNotNone(result["optimal_vector"])
        self.assertIn("exploratory", result["explanation"])

    @staticmethod
    def run_endpoint(stream, answers):
        import asyncio

        return asyncio.run(
            main.analyze_quiz(main.QuizPayload(stream=stream, answers=answers))
        )


if __name__ == "__main__":
    unittest.main()
