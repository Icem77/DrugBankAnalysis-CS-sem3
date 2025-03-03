import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from part9 import group_sizes_df, count_approved_and_not_withdrawn, percentage_of_withdrawned_after_approval_pie_chart

if __name__ == "__main__":
    frame = group_sizes_df("drugbank_partial_and_generated.xml")
    approved_and_not_withdrawn = count_approved_and_not_withdrawn("drugbank_partial_and_generated.xml")

    print(frame)
    print()
    print(f"Approved and not withdrawn: {approved_and_not_withdrawn}")

    percentage_of_withdrawned_after_approval_pie_chart(
        frame,
        approved_and_not_withdrawn
    )
