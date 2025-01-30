import torch
from transformers import AutoModelForTokenClassification
from .pipeline import Pipeline


class TokenClassificationPipeline(Pipeline):
    name = "token-classification"
    model_class = AutoModelForTokenClassification
    default_tokenize_args = dict(padding=False,truncation=True, max_length=512, return_offsets_mapping=True)
    dataset_cols = ["input_ids", "attention_mask", "offset_mapping", "idx"]

    def init_preds(self, dataset, **kwargs):
        max_len = max(len(x) for x in dataset["input_ids"])
        def pad_offset_mapping(inputs):
            offset_mapping = []
            for i in range(len(inputs['offset_mapping'])):
                padding = torch.tensor([[0, 0]] * (max_len - len(inputs['offset_mapping'][i])))
                padded_offset_mapping = torch.cat([inputs['offset_mapping'][i], padding], dim=0)
                offset_mapping.append(padded_offset_mapping)
            return dict(offset_mapping=offset_mapping)
        dataset = dataset.map(pad_offset_mapping, batched=True)
        return dataset, torch.empty(len(dataset), max_len)

    def process_outputs(self, outputs, **kwargs):
        return outputs.logits.argmax(dim=-1)
    
    def post_process_preds(self, examples, preds, dataset, **kwargs):
        id2label = self.model.config.id2label
        offset_mappings = dataset["offset_mapping"]

        results = []
        for i, text in enumerate(examples):
            token_ids = preds[i]
            offsets = offset_mappings[i]
            spans = []
            for tok_idx, label_id in enumerate(token_ids):
                label_id = label_id.item()
                if label_id == -1:
                    break
                label = id2label[label_id]
                start, end = offsets[tok_idx]
                if label.startswith("B-"):
                    spans.append({"start": start.item(), "end": end.item(), "label": label})
                elif label.startswith("I-"):
                    spans[-1]["end"] = end.item()
            results.append(spans)
        return results



class NERPipeline(TokenClassificationPipeline):
    name = 'ner'
