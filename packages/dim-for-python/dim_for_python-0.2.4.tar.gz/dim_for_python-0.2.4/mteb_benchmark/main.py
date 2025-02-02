import asyncio

import mteb
import numpy as np
from dim_python import vectorize_string
from mteb.encoder_interface import PromptType


class DimStringVectorization:
    def encode(
        self,
        sentences: list[str],
        task_name: str = "",
        prompt_type: PromptType | None = None,
        **kwargs,
    ) -> np.ndarray:
        """Encodes the given sentences using the encoder.
        
        Args:
            sentences: The sentences to encode.
            task_name: The name of the task.
            prompt_type: The prompt type to use.
            **kwargs: Additional arguments to pass to the encoder.
            
        Returns:
            The encoded sentences.
        """
        encoded_sentences = []
        
        loop = asyncio.get_event_loop()
        
        for sentence in sentences:
            encoded_sentences.append(
                loop.run_until_complete(run(sentence))
            )
       
        for encoded_sentence in encoded_sentences:
            print(encoded_sentence)
        
        return np.array(encoded_sentences)


async def run(sentence: str) -> list[float]:
    return await vectorize_string(
        string=sentence,
        prompts = [
            "Given a text input, label it according to the provided categories and output the result in JSON format. STRICTLY ADHERE TO THIS FORMAT: {'numeric_label': your score}\n activate_my_card: 0, age_limit: 1, apple_pay_or_google_pay: 2, atm_support: 3, automatic_top_up: 4, balance_not_updated_after_bank_transfer: 5, balance_not_updated_after_cheque_or_cash_deposit: 6, beneficiary_not_allowed: 7, cancel_transfer: 8, card_about_to_expire: 9, card_acceptance: 10, card_arrival: 11, card_delivery_estimate: 12, card_linking: 13, card_not_working: 14, card_payment_fee_charged: 15, card_payment_not_recognised: 16, card_payment_wrong_exchange_rate: 17, card_swallowed: 18, cash_withdrawal_charge: 19, cash_withdrawal_not_recognised: 20, change_pin: 21, compromised_card: 22, contactless_not_working: 23, country_support: 24, declined_card_payment: 25, declined_cash_withdrawal: 26, declined_transfer: 27, direct_debit_payment_not_recognised: 28, disposable_card_limits: 29, edit_personal_details: 30, exchange_charge: 31, exchange_rate: 32, exchange_via_app: 33, extra_charge_on_statement: 34, failed_transfer: 35, fiat_currency_support: 36, get_disposable_virtual_card: 37, get_physical_card: 38, getting_spare_card: 39, getting_virtual_card: 40, lost_or_stolen_card: 41, lost_or_stolen_phone: 42, order_physical_card: 43, passcode_forgotten: 44, pending_card_payment: 45, pending_cash_withdrawal: 46, pending_top_up: 47, pending_transfer: 48, pin_blocked: 49, receiving_money: 50, Refund_not_showing_up: 51, request_refund: 52, reverted_card_payment?: 53, supported_cards_and_currencies: 54, terminate_account: 55, top_up_by_bank_transfer_charge: 56, top_up_by_card_charge: 57, top_up_by_cash_or_cheque: 58, top_up_failed: 59, top_up_limits: 60, top_up_reverted: 61, topping_up_by_card: 62, transaction_charged_twice: 63, transfer_fee_charged: 64, transfer_into_account: 65, transfer_not_received_by_recipient: 66, transfer_timing: 67, unable_to_verify_identity: 68, verify_my_identity: 69, verify_source_of_funds: 70, verify_top_up: 71, virtual_card_not_working: 72, visa_or_mastercard: 73, why_verify_identity: 74, wrong_amount_of_cash_received: 75, wrong_exchange_rate_for_cash_withdrawal: 76"
        ],
        model="mistral",
        api_key="sk-1234",
        base_url="http://192.168.0.101:11434/v1"
    )


if __name__ == "__main__":
    
    import logging

    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    logger.info("Starting the model evaluation")

    model = DimStringVectorization()
    tasks = mteb.get_tasks(tasks=["Banking77Classification"])
    evaluation = mteb.MTEB(tasks=tasks)
    evaluation.run(model, verbosity=2)

    logger.info("Model evaluation completed")
    
#     print(asyncio.run(run("I am happy")))
    
#     for _ in range(10):
#         print(model.encode(["I am happy", "I am sad"]))