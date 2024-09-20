examples = [
    {
        "inputs": {
            "question": "How does that apply?",
            "chat_history": [
                {
                    "role": "user",
                    "content": "I’m trying tto uunderstand instein’s theory.",
                },
                {
                    "role": "assistant",
                    "content": "Which one? He's known for several theories.",
                },
                {"role": "user", "content": "Thee one about time and spae."},
                {
                    "role": "assistant",
                    "content": "Ah, you're referring to the theory of relativity. There are two parts: special and general. Which one?",
                },
            ],
        },
        "outputs": {
            "expected": "Special relativity, proposed by Einstein in 1905, deals with objects in uniform motion, especially those moving at the speed of light. It introduced the idea that time and space are relative and can change in relation to each other. For instance, time can appear to move slower for an object moving close to the speed of light."
        },
    },
    {
        "inputs": {
            "question": "What's the main difference?",
            "chat_history": [
                {"role": "user", "content": "Can yyou contrast DNA and RNA for me?"},
                {
                    "role": "assistant",
                    "content": "Certainly. DNA and RNA are both nucleic acids but have different roles, structures, and properties. Do you want specifics?",
                },
            ],
        },
        "outputs": {
            "expected": "The main structural differences between DNA and RNA include: 1) DNA is double-stranded while RNA is single-stranded. 2) The sugar in the backbone of RNA is ribose, whereas in DNA it's deoxyribose. 3) DNA uses the bases adenine (A), cytosine (C), guanine (G), and thymine (T); RNA uses adenine (A), cytosine (C), guanine (G), and uracil (U) instead of thymine."
        },
    },
    {
        "inputs": {
            "question": "what led them to such a draastic action?",
            "chat_history": [
                {"role": "user", "content": "tell me about the Boston Tea Party."},
                {
                    "role": "assistant",
                    "content": "The Boston Tea Party was a political protest by the American colonists against the British government in 1773. They were protesting the Tea Act, which allowed the British East India Company to sell tea directly to the colonies, bypassing colonial merchants.",
                },
            ],
        },
        "outputs": {
            "expected": "The colonists undertook the Boston Tea Party as a drastic action due to multiple reasons: 1) They believed the Tea Act was a violation of their rights as Englishmen, as they were being taxed without their consent. 2) The act gave the British East India Company a monopoly on tea sales, threatening local businesses. 3) The act was seen as another example of the British government's increasing interference in colonial affairs. The protest was a way to show their strong opposition to British policies."
        },
    },
    {
        "inputs": {
            "question": "thats a scary one. can it be avoideed?",
            "chat_history": [
                {"role": "user", "content": "I'm learning bout genetic disorders."},
                {
                    "role": "assistant",
                    "content": "Genetic disorders are diseases caused by abnormalities in an individual's DNA. They can be inherited or result from mutations. One common one is Huntington's disease.",
                },
            ],
        },
        "outputs": {
            "expected": "Huntington's disease is a hereditary genetic disorder caused by a mutation in the HTT gene. If a person inherits the defective gene, they will eventually develop the disease. Currently, there's no cure for Huntington's, but its onset can be delayed with treatment. Genetic counseling and testing can help prospective parents understand the risks of passing the mutation to their offspring."
        },
    },
    {
        "inputs": {
            "question": "Which one?",
            "chat_history": [
                {
                    "role": "user",
                    "content": "I'm confused aboutt stars. what even aaaare they?",
                },
                {
                    "role": "assistant",
                    "content": "Stars are celestial bodies made mostly of hydrogen and helium. They generate light and heat through nuclear fusion in their cores.",
                },
                {
                    "role": "user",
                    "content": "there''s a classification based on theirbrightness, right?",
                },
                {
                    "role": "assistant",
                    "content": "Yes",
                },
            ],
        },
        "outputs": {
            "expected": "Yes, stars are classified based on their brightness using a system called the Hertzsprung-Russell (H-R) diagram. In this diagram, stars are categorized into main-sequence stars, giants, supergiants, and white dwarfs, based on their luminosity and temperature. The Sun, for instance, is a main-sequence star."
        },
    },
]