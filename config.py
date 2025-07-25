PDF_URLS = [
    "https://developer.nbg.gr/sites/default/files/PromptEngineeringF.pdf",
    "https://www.developer.tech.gov.sg/products/collections/data-science-and-artificial-intelligence/playbooks/prompt-engineering-playbook-beta-v3.pdf",
    "https://www.cluedin.com/hubfs/Whitepapers/Beginners-guide-to-prompt-egineering.pdf",
    "https://www.cse.iitd.ac.in/~mausam/courses/col772/spring2023/lectures/22-promptengg.pdf",
    "https://github.com/dair-ai/Prompt-Engineering-Guide/blob/main/lecture/Prompt-Engineering-Lecture-Elvis.pdf",
    "https://static.skillshare.com/uploads/attachment/1215140161/87dc02f9/THE%20PROMPT%20ENGINEERING%20GUIDE%20V2.pdf.pdf",
    "https://www.tutorialspoint.com/prompt_engineering/prompt_engineering_tutorial.pdf"
]

SCHEMA_CONFIG = {
    "class": "Document",
    "vectorizer": "none",
    "properties": [
        {"name": "text", "dataType": ["text"]},
        {"name": "source", "dataType": ["text"]}
    ]
}
