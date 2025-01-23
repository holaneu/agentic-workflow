# Agentic Workflow

## App Overview
- **App Name:** Agentic Workflow
- **App Description:** A flexible AI-powered text processing system that enables various language-based workflows using multiple AI models.

## Core Functionality:

### Features:
- **Multi-Model Support**: Integration with multiple AI providers (OpenAI, Mistral, Google, Anthropic)
- **Workflow System**: Predefined workflows for common text processing tasks
- **File Management**: Automated output handling and logging system
- **API Integration**: Unified interface for different AI model providers

### User Actions (Stories)
**As a user** I want to:
- Process text through different AI workflows
- Choose between different AI models for processing
- Save and track processing results
- Access different text processing functions (translation, summarization)

## App Layout and UI Elements

### **Main Interface Screen:**
- **Purpose:** Text input and workflow selection
- **Content:** Input form, workflow selector
- **UI Elements**: Text area, workflow dropdown, submit button
- **Navigation:** Simple single-page interface

### **Available Workflows:**
- **Translation (CS-EN)**: 
  - Translates between Czech and English
  - Uses Gemini 1.5 Flash model
- **Text Summarization**: 
  - Creates concise summaries of input text
  - Uses GPT-4 Mini model

## Technical Specifications
- Python/Flask backend
- Environment-based configuration
- Supported AI Models:
  - GPT-4 Mini (OpenAI)
  - Mistral Small
  - Gemini 1.5 Flash
  - Claude 3 Haiku
- File-based output system
- Comprehensive error handling

## Future Enhancements
- **Additional Workflows**: Expand available text processing options
- **Model Selection**: Allow users to choose specific models for each workflow
- **Batch Processing**: Support for processing multiple texts
- **Results History**: View and manage previous processing results
- **API Extension**: Add support for more AI providers and models
