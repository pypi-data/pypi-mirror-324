/** @odoo-module **/

import {CharField, charField} from "@web/views/fields/char/char_field";
import {patch} from "@web/core/utils/patch";

// Adding a new property for dynamic placeholder button visibility
CharField.props = {
    ...CharField.props,
    dynamicPlaceholderButtonField: {type: String, optional: true},
    dynamicPlaceholderConverterField: {type: String, optional: true},
};

// Extending charField to extract the new property
const charExtractProps = charField.extractProps;
charField.extractProps = (fieldInfo) => {
    return Object.assign(charExtractProps(fieldInfo), {
        dynamicPlaceholderButtonField:
            fieldInfo.options?.dynamic_placeholder_button_field,
        dynamicPlaceholderConverterField:
            fieldInfo.options?.dynamic_placeholder_converter_field,
    });
};

// Patching CharField to include the visibility check
patch(CharField.prototype, {
    setup() {
        super.setup();
    },
    get hasDynamicPlaceholderButton() {
        return !this.props.record.data[this.props.dynamicPlaceholderButtonField];
    },
    get converter() {
        return (
            this.props.record.data[this.props.dynamicPlaceholderConverterField] || ""
        );
    },
    async onDynamicPlaceholderValidate(chain, defaultValue) {
        if (chain) {
            this.input.el.focus();
            // Initialize dynamicPlaceholder with a default structure
            let dynamicPlaceholder = ` {{object.${chain}${
                defaultValue?.length ? ` ||| ${defaultValue}` : ""
            }}}`;
            switch (this.converter) {
                case "field":
                    // For "field" converter, use the chain directly as the value
                    dynamicPlaceholder = `${chain}`;
                    break;

                default:
                    // Default case if no specific converter type is found
                    dynamicPlaceholder = ` {{object.${chain}${
                        defaultValue?.length ? ` ||| ${defaultValue}` : ""
                    }}}`;
                    break;
            }
            this.input.el.setRangeText(
                dynamicPlaceholder,
                this.selectionStart,
                this.selectionStart,
                "end"
            );
            // trigger events to make the field dirty
            this.input.el.dispatchEvent(new InputEvent("input"));
            this.input.el.dispatchEvent(new KeyboardEvent("keydown"));
            this.input.el.focus();
        }
    },
});
