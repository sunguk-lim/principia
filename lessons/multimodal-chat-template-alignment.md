# Multimodal Chat Template Alignment

## Meaning

A vision-language model does not train on an abstract list of messages. Its processor renders roles, image placeholders, special tokens, and answer boundaries into model inputs. **Chat-template alignment** means that training examples and inference prompts use the intended model-specific representation and that labels cover the intended output, not hidden reasoning or prompt tokens by accident.

## Mechanism

The [[multimodal-input-contract]] specifies which image and text parts the API accepts; the template specifies how the processor serializes them for the model. A training sample may contain an image plus an instruction in a user turn and a one-line LaTeX answer in an assistant turn. Before [[fine-tuning]], render a sample with the official processor and inspect the token/placeholder sequence and label mask. Handwritten formatting borrowed from another model can silently put the image marker, channel name, or end-of-turn token in the wrong place.

At inference, use the same processor and the correct generation boundary. Some models have separate analysis and answer channels or adjustable reasoning effort; those are model-specific controls, not a universal chat standard. If training labels contain only direct answers but inference begins in a reasoning channel, the system may waste tokens or fail to emit the expected answer. Conversely, forcing an answer channel can change model behavior; test it rather than assuming improvement.

## One example

For image-to-LaTeX training, render one image-plus-instruction sample with the official processor and verify the answer tokens, image placeholder, and label mask.

## Check your understanding

**Question:** Why can a text-only template be wrong for a vision model?

**Answer:** It may omit image content processing or use the wrong special tokens and channel boundaries.
