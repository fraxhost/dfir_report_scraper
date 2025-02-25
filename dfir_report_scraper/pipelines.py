# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class DescriptionCleanupPipeline:

    def process_item(self, item, spider):
        # Use ItemAdapter to interact with the item fields
        adapter = ItemAdapter(item)

        if "description" in adapter:
            description = adapter["description"]

            # Split the description based on sentences using your logic
            merged_array = []
            temp_sentence = ""

            # Merging fragmented sentences
            for part in description:
                temp_sentence += part.strip()
                if re.search(
                    r"[.!?]$", temp_sentence
                ):  # If sentence ends with a valid delimiter
                    merged_array.append(temp_sentence)
                    temp_sentence = ""

            # Add any remaining fragment
            if temp_sentence:
                merged_array.append(temp_sentence)

            # Final array to hold the split sentences
            new_array = []
            for sentence in merged_array:
                # Splitting while keeping the delimiter and avoiding splitting i.e. or e.g.
                split_sentences = re.split(r"(?<!\b(?:i\.e|e\.g))([.!?])\s+", sentence)
                new_sentence = ""
                for i, part in enumerate(split_sentences):
                    if (
                        part in ".!?"
                    ):  # If it's a delimiter, append it and store the full sentence
                        new_sentence += part
                        new_array.append(
                            new_sentence.strip()
                        )  # Store the completed sentence
                        new_sentence = ""
                    else:
                        # If it's not a delimiter, append the part without extra space
                        if i > 0:
                            new_sentence += " "  # Add a space only after the first part
                        new_sentence += part.strip()  # Append next part

            # Clean up any trailing spaces
            new_array = [s.strip() for s in new_array if s.strip()]

            # Update the item with the modified description using ItemAdapter
            adapter["description"] = new_array

        return item
