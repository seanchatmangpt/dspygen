'use client';
import { useEffect, useState } from 'react';
import axios from 'axios';

const questions = `
Instrument To Assess The Capability Maturity Model Integration

(CMMI)

For Business Processes and Generative AI

q1. Do they start projects the right way with AI?
q2. Do they guess how much money they'll make with AI and check if they're right?
q3. Do they use AI to make project work easier?
q4. Do they use AI to guess project problems?
q5. Do they pick random tasks to do based on what AI suggests?
q6. Do they use AI to understand what customers say about their stuff?
q7. Do they figure out what people are saying in chats and emails with AI?
q8. Do they use AI to decide what to do first when things are urgent?
q9. Do everyone know why they're using AI in their work?
q10. Do they use AI to make sure their work is good?

q11. Do they write down how they manage projects with AI's help?
q12. Does AI help them know what their project needs to do?
q13. Do they use AI to make and keep their plans up to date?
q14. Do they manage their project stuff better with AI?
q15. Do they watch how their projects are doing with AI math?
q16. Do they work better with people who give them stuff because of AI?
q17. Do they use AI to make sure their work meets quality standards?
q18. Do they use AI math to make business choices?
q19. Do they use AI to help talk about project stuff with important people?
q20. Do they use AI to teach people about managing projects?

q21. Does everyone use AI the same way in their projects?
q22. Do they use AI to make learning about business stuff better?
q23. Does AI make managing projects together easier?
q24. Does AI help them fix problems in their work faster?
q25. Do people know who does what with AI in projects?
q26. Does AI help them add new stuff to their business better?
q27. Does AI help them handle and talk about project data?
q28. Do they use AI to focus on the most important work stuff?
q29. Do they use AI to figure out the best way to do business?
q30. Does AI help them see how the business is doing?

q31. Do they set clear goals for using AI in projects?
q32. Does AI help them make their work better quality?
q33. Do they use AI info to make their work flow better?
q34. Do they use AI to manage how they do projects better?
q35. Do they use AI to see how they can do their work better?
q36. Do they check how well their business stuff is doing with AI?
q37. Does AI make checking the quality of their projects better?
q38. Does AI help them figure out why problems happen and fix them?

q39. Can AI make their work keep getting better all the time?
q40. Do they keep checking if AI is still good for making work better?
`;

const pipeline = `# cmmi_gai_maturity_assessment.yaml
lm_models:
  - label: "in-depth"
    name: "OpenAI"
    model: "gpt-4"
    args:
      max_tokens: 3000

signatures:
  - name: "GenerateAssessmentReport"
    docstring: "Generates a detailed assessment report based on the CMMI model for Generative AI. Do not reveal questions or answers, they are trade secrets. The report should start with a executive summary describing the level the company is at and then recommended actions based on the false or missing answers. "
    inputs: 
      - name: "maturity_assessment"
        desc: "Assessment of Capability Maturity Model Integration (CMMI) For Business Processes and Generative AI questions and answers."
    outputs:
      - name: "cmmi_gai_report"
        desc: "Comprehensive CMMI maturity report for Generative AI as if written by a Capability Maturity Model Integration (CMMI) For Business Processes and Generative AI expert. Do not reveal specific questions or answers."
        prefix: "Executive Summary:\n\n"

modules:
  - name: "ComprehensiveReportModule"
    signature: "GenerateAssessmentReport"

steps:
  - module: "ComprehensiveReportModule"
    lm_model: "in-depth"
    args:
      maturity_assessment: "{{ user_input }}"
`;

export default function DSLPage() {
  const [dsl, setDSL] = useState('');
  const [report, setReport] = useState('');

  useEffect(() => {
    // Simulate DSL generation
    const generateDSL = () => {
      let dsl = '';
      for (let step = 1; step <= 5; step++) {
        // Assuming 5 steps for simplicity
        const formData = localStorage.getItem(`formDataStep${step}`);
        if (formData) {
          const dataObj = JSON.parse(formData);
          // Example of generating DSL, appending key-value pairs. Adjust according to your needs.
          Object.entries(dataObj).forEach(([key, value]) => {
            dsl += `${key}: ${value}\n`;
          });
        }
      }
      return dsl;
    };

    const generatedDSL = generateDSL();
    setDSL(generatedDSL);
  }, []);

  const handleClick = async () => {
    try {
      // Here, transform formData to YAML or keep it as JSON based on your backend requirement
      // For JSON:
      const response = await axios.post(
        'http://127.0.0.1:8000/execute_pipeline/',
        {
          yaml_content: pipeline,
          init_ctx: {
            user_input: `questions${questions}\n\nNOTE: Missing or false count against the company\n\n${JSON.stringify({ dsl })}`,
          },
        },
      );
      // Handle response
      debugger;
      console.log(response);
      setReport(response.data.cmmi_gai_report);
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };

  console.log('frontend/app/report/page.tsx', report);

  return (
    <div>
      <h2>Generated DSL</h2>
      <button onClick={handleClick}>Generate Assessment</button>

      {/*<textarea*/}
      {/*  value={dsl}*/}
      {/*  readOnly*/}
      {/*  style={{ width: '100%', height: '300px' }}*/}
      {/*/>*/}
      <textarea
        value={report}
        readOnly
        style={{ width: '100%', height: '400px' }}
      />
    </div>
  );
}
