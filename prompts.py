"""
Prompt templates and generation logic for research article summarization.
Contains all prompting methods and their corresponding templates.
"""
import re
from typing import Dict, Callable

class PromptGenerator:
    """Handles generation of prompts for different prompting methods."""
    
    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text"""
        words = re.findall(r'\b\w+\b', text.strip())
        return len(words)
    
    @staticmethod
    def validate_article(article: str) -> tuple[bool, str]:
        """Validate article length and content"""
        if not article or not article.strip():
            return False, "Article content is required"
        
        word_count = PromptGenerator.count_words(article)
        
        if word_count < 500:
            return False, f"Article too short ({word_count} words). Minimum 500 words required."
        
        if word_count > 1000:
            return False, f"Article too long ({word_count} words). Maximum 1000 words allowed."
        
        return True, f"Article length valid ({word_count} words)"
    
    @staticmethod
    def create_chain_of_thoughts_prompt(article: str) -> str:
        """Chain-of-Thoughts: Step-by-step reasoning"""
        return f"""I need to summarize this research article step by step. Let me think through this systematically:

Step 1: First, I'll identify the background and context
Step 2: Then, I'll extract the research objectives
Step 3: Next, I'll understand the methodology used
Step 4: After that, I'll identify the key results
Step 5: Finally, I'll determine the main takeaways

Let me work through each step:

Research Article:
{article}

Now, let me create a comprehensive summary following my step-by-step analysis:

Please provide a single paragraph summary (up to 150 words) that includes background, objectives, methodology, results, and takeaways based on my systematic analysis above."""

    @staticmethod
    def create_tree_of_thoughts_prompt(article: str) -> str:
        """Tree-of-Thoughts: Multiple reasoning paths"""
        return f"""I will analyze this research article using multiple reasoning paths and then synthesize the best insights:

Path 1: Academic Analysis Approach
- Focus on scholarly rigor and methodology
- Emphasize research contribution and novelty

Path 2: Practical Application Approach  
- Focus on real-world implications
- Emphasize actionable insights

Path 3: Critical Evaluation Approach
- Focus on limitations and strengths
- Emphasize balanced perspective

Research Article:
{article}

Now, synthesizing insights from all three reasoning paths, provide a comprehensive single paragraph summary (up to 150 words) that captures the background, objectives, methodology, results, and key takeaways."""

    @staticmethod
    def create_role_based_prompt(article: str) -> str:
        """Role-based: Acting as a research expert"""
        return f"""You are a senior research analyst with 20 years of experience in academic literature review and synthesis. Your expertise lies in quickly identifying key research components and distilling complex studies into clear, actionable summaries.

As an expert research analyst, your task is to:
1. Quickly scan and identify the research background and motivation
2. Extract the core research objectives and hypotheses
3. Understand the methodological approach and its appropriateness
4. Identify the most significant results and findings
5. Synthesize the key implications and contributions

Research Article to Analyze:
{article}

Based on your expert analysis, provide a single paragraph summary (up to 150 words) that covers background, objectives, methodology, results, and takeaways in a professional, academic tone."""

    @staticmethod
    def create_react_prompt(article: str) -> str:
        """ReAct: Reasoning and Acting iteratively"""
        return f"""I'll use the ReAct approach (Reasoning + Acting) to analyze this research article:

Thought 1: I need to understand what this research is about
Action 1: Read and identify the research domain and context
Observation 1: [After reading] I can see the background and motivation

Thought 2: I should extract the specific research goals
Action 2: Identify the research questions and objectives
Observation 2: [After analysis] I understand what the researchers aimed to achieve

Thought 3: I need to understand how they conducted the research
Action 3: Analyze the methodology and approach used
Observation 3: [After review] I can see their research methods

Thought 4: I should identify what they discovered
Action 4: Extract the key results and findings
Observation 4: [After examination] I understand their main findings

Thought 5: I need to synthesize the implications
Action 5: Determine the key takeaways and contributions
Observation 5: [After synthesis] I can summarize the significance

Research Article:
{article}

Based on my ReAct analysis above, provide a single paragraph summary (up to 150 words) covering background, objectives, methodology, results, and takeaways."""

    @staticmethod
    def create_directional_stimulus_prompt(article: str) -> str:
        """Directional Stimulus: Guiding toward desired output"""
        return f"""Focus your analysis on creating a structured research summary that academic reviewers would find comprehensive and valuable. Your summary should demonstrate deep understanding of research methodology and significance.

Key directions for your analysis:
→ Background: What problem or gap motivated this research?
→ Objectives: What specific questions did the researchers seek to answer?
→ Methodology: What approach did they use and why was it appropriate?
→ Results: What were the most important findings and discoveries?
→ Takeaways: What are the broader implications and future directions?

Research Article:
{article}

Following these directions, create a single paragraph summary (up to 150 words) that would satisfy academic standards for research comprehension and synthesis."""

    @staticmethod
    def create_step_back_prompt(article: str) -> str:
        """Step-Back: Higher-level perspective first"""
        return f"""Before diving into the details, let me step back and consider the bigger picture:

High-level question: What is the overarching contribution of this research to its field?
Broader context: How does this work fit into the larger landscape of research in this area?
Meta-question: What makes this research important and worth summarizing?

Now, with this broader perspective in mind, let me analyze the specific details:

Research Article:
{article}

Using both the high-level perspective and detailed analysis, provide a single paragraph summary (up to 150 words) that captures the background, objectives, methodology, results, and key takeaways while maintaining awareness of the research's broader significance."""

    @staticmethod
    def create_zero_shot_prompt(article: str) -> str:
        """Zero-shot: Direct instruction without examples"""
        return f"""Summarize the following research article in exactly one paragraph of up to 150 words. Your summary must include the background context, research objectives, methodology used, key results obtained, and main takeaways. Write in a clear, academic style.

Research Article:
{article}

Provide your summary now."""

    @staticmethod
    def create_one_shot_prompt(article: str) -> str:
        """One-shot: One example to guide the format"""
        return f"""Here's an example of how to summarize a research article:

Example Article: "A study on machine learning algorithms for medical diagnosis..."
Example Summary: "This research addresses the growing need for accurate automated medical diagnosis systems by investigating machine learning approaches in clinical settings. The study aimed to compare the effectiveness of three ML algorithms (neural networks, decision trees, and SVM) in diagnosing cardiovascular diseases. The researchers used a dataset of 5,000 patient records and employed cross-validation techniques to ensure robustness. Results showed that neural networks achieved 94% accuracy, significantly outperforming the other methods. The key takeaway is that neural network-based systems can provide reliable diagnostic support for healthcare professionals, potentially reducing misdiagnosis rates and improving patient outcomes in resource-limited settings."

Now, following the same format and style, summarize this research article in one paragraph (up to 150 words):

Research Article:
{article}"""

    @staticmethod
    def create_few_shot_prompt(article: str) -> str:
        """Few-shot: Multiple examples to guide the format"""
        return f"""Here are examples of how to summarize research articles:

Example 1:
Article: "Climate change impact on agricultural productivity..."
Summary: "This study investigates the relationship between climate change and agricultural productivity in developing nations, motivated by concerns about food security. The research aimed to quantify how temperature and precipitation changes affect crop yields across different regions. Using satellite data and statistical modeling over 20 years, researchers analyzed yield patterns for major crops. Results revealed a 15% average decline in productivity, with wheat and rice most affected. The key takeaway is that adaptive farming strategies and climate-resilient crops are urgently needed to maintain food security in vulnerable regions."

Example 2:
Article: "Social media influence on consumer behavior..."
Summary: "This research examines how social media platforms shape consumer purchasing decisions, addressing the gap in understanding digital marketing effectiveness. The study sought to identify which social media factors most influence buying behavior across different demographics. Through surveys of 2,000 consumers and analysis of social media engagement data, researchers used regression analysis to identify key predictors. Findings showed that peer reviews and influencer endorsements increased purchase likelihood by 40%. The main takeaway is that businesses should prioritize authentic social proof and influencer partnerships to optimize their digital marketing strategies."

Now, following the same format and style as these examples, summarize this research article in one paragraph (up to 150 words):

Research Article:
{article}"""

    @classmethod
    def create_prompt_by_method(cls, article: str, method: str) -> str:
        """Create prompt based on selected method"""
        prompt_methods: Dict[str, Callable[[str], str]] = {
            'chain_of_thoughts': cls.create_chain_of_thoughts_prompt,
            'tree_of_thoughts': cls.create_tree_of_thoughts_prompt,
            'role_based': cls.create_role_based_prompt,
            'react': cls.create_react_prompt,
            'directional_stimulus': cls.create_directional_stimulus_prompt,
            'step_back': cls.create_step_back_prompt,
            'zero_shot': cls.create_zero_shot_prompt,
            'one_shot': cls.create_one_shot_prompt,
            'few_shot': cls.create_few_shot_prompt
        }
        
        if method in prompt_methods:
            return prompt_methods[method](article)
        else:
            return cls.create_zero_shot_prompt(article)  # Default fallback


# Available prompting methods
PROMPTING_METHODS = {
    'chain_of_thoughts': 'Chain-of-Thoughts',
    'tree_of_thoughts': 'Tree-of-Thoughts', 
    'role_based': 'Role-based prompting',
    'react': 'ReAct prompting',
    'directional_stimulus': 'Directional Stimulus prompting',
    'step_back': 'Step-Back prompting',
    'zero_shot': 'Zero-shot',
    'one_shot': 'One-shot',
    'few_shot': 'Few-shot'
} 