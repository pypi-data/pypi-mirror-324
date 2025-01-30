from odoo import fields, models  # type: ignore[import-untyped]


class MailComposer(models.TransientModel):
    _inherit = "mail.compose.message"

    is_redner_template = fields.Boolean(related="template_id.is_redner_template")

    def get_mail_values(self, res_ids):
        """
        Overrides the get_mail_values method to enhance email value retrieval
        based on mass mail mode and redner template.
        """
        all_mail_values = super().get_mail_values(res_ids)
        mass_mail_mode = self.composition_mode == "mass_mail"

        # Check if in mass mail mode and if redner template exists
        if mass_mail_mode and self.model and self.template_id.is_redner_template:
            template_values = self.generate_email_for_composer(
                self.template_id.id, res_ids, ["body_html"]
            )

            # Update email values with rendered content
            for res_id in res_ids:
                body = template_values[res_id]["body"]
                all_mail_values[res_id].update({"body": body, "body_html": body})

        return all_mail_values
