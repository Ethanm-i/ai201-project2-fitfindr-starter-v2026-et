"""Check real search and session handoffs without making model requests."""

import unittest
from pprint import pprint
from unittest.mock import patch

import agent
from utils.data_loader import get_example_wardrobe, get_empty_wardrobe


class AgentTests(unittest.TestCase):
    def test_empty_wardrobe(self):
        with patch("tools.generate", side_effect=["Pair it with neutral basics.", "A thrift find."]) as model:
            session = agent.run_agent("graphic tee", get_empty_wardrobe())
        self.assertIsNone(session["error"])
        self.assertTrue(session["outfit_suggestion"].strip())
        self.assertIn("general styling advice", model.call_args_list[0].args[0])

    def test_model_unavailable(self):
        for failed_call in (1, 2):
            with self.subTest(failed_call=failed_call):
                responses = ["Pair it with jeans."] * (failed_call - 1)
                responses.append(agent.ModelUnavailable("Invalid API key"))
                with patch("tools.generate", side_effect=responses) as model:
                    session = agent.run_agent("graphic tee", get_example_wardrobe())
                self.assertIn("model couldn't be reached", session["error"])
                self.assertIn("GEMINI_API_KEY", session["error"])
                self.assertIsNone(session["fit_card"])
                self.assertEqual(model.call_count, failed_call)

    def test_happy_path(self):
        with patch("tools.generate", side_effect=[
            "Pair the tee with jeans and sneakers.",
            "A thrifted tee for an easy everyday outfit.",
        ]), patch("agent.suggest_outfit", wraps=agent.suggest_outfit) as outfit, \
                patch("agent.create_fit_card", wraps=agent.create_fit_card) as card:
            session = agent.run_agent(
                "vintage graphic tee under $30, size M", get_example_wardrobe()
            )
        self.assertIsNone(session["error"])
        self.assertEqual(session["parsed"]["max_price"], 30)
        self.assertEqual(session["parsed"]["size"], "M")
        self.assertEqual(session["parsed"]["description"], "vintage graphic tee")
        self.assertIs(session["selected_item"], session["search_results"][0])
        self.assertIs(outfit.call_args.args[0], session["selected_item"])
        self.assertIs(outfit.call_args.args[1], session["wardrobe"])
        self.assertEqual(card.call_args.args[0], session["outfit_suggestion"])
        self.assertIs(card.call_args.args[1], session["selected_item"])
        self.assertTrue(session["fit_card"])
        print("\nHappy-path session (controlled model responses):")
        pprint(session, sort_dicts=False)
        print("PASS: suggest_outfit received the exact selected item.")

    def test_no_matches(self):
        with patch("agent.suggest_outfit") as outfit, \
                patch("agent.create_fit_card") as card:
            session = agent.run_agent(
                "designer ballgown size XXS under $5", get_example_wardrobe()
            )
        self.assertEqual(session["search_results"], [])
        self.assertIsNone(session["selected_item"])
        self.assertIsNone(session["outfit_suggestion"])
        self.assertIsNone(session["fit_card"])
        self.assertIn("different keywords", session["error"])
        self.assertIn("price limit", session["error"])
        self.assertIn("size filter", session["error"])
        outfit.assert_not_called()
        card.assert_not_called()
        print("\nNo-match session (real search):")
        pprint(session, sort_dicts=False)


if __name__ == "__main__":
    unittest.main()
