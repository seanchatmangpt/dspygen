'use client';
import { usePathname, useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import Form, { IChangeEvent } from '@rjsf/core';
import jsYaml from 'js-yaml';
import validator from '@rjsf/validator-ajv8';
import { useRouter } from 'next/navigation';

export default function Page({
  searchParams,
}: {
  searchParams?: {
    step?: string;
  };
}) {
  const router = useRouter(); // Get the router instance
  const pathname = usePathname();
  const step = parseInt((searchParams?.step as string) || '1', 10);

  const [schema, setSchema] = useState({});
  const [formData, setFormData] = useState({});

  const onSubmit = (e: IChangeEvent<any>) => {
    const formData = e.formData;
    localStorage.setItem(`formDataStep${step}`, JSON.stringify(formData));

    if (step < 5) {
      const nextStep = step + 1;
      router.push(`${pathname}?step=${nextStep}`); // Navigate to the next step
    } else {
    }
  };

  const generateDSLFromFormData = (allData) => {
    // Implement this function to convert form data to DSPyGen DSL
  };

  const generateAndSendDSL = () => {
    const allFormData = {};
    for (let i = 1; i <= 5; i++) {
      Object.assign(
        allFormData,
        JSON.parse(localStorage.getItem(`formDataStep${i}`) || '{}'),
      );
    }
    const dsl = generateDSLFromFormData(allFormData);
    const yamlContent = jsYaml.dump(dsl);

    // Execute the pipeline
    fetch('/api/execute_pipeline', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ yaml_content: yamlContent }),
    })
      .then((res) => res.json())
      .then((data) => {
        // Navigate to results, passing data through query params or another method
        // setSearchParams({ step: 'results', ...data });
      })
      .catch(console.error);
  };

  const validateFormData = (formData, errors) => {
    // Example validation: Ensure 'firstName' field is not empty
    console.log(formData);

    return errors;
  };

  return (
    <div>
      {step <= 5 ? (
        <Form
          schema={schema}
          formData={formData}
          onSubmit={onSubmit}
          validator={validator}
        />
      ) : (
        <div>Show results here based on query params or another method</div>
      )}
    </div>
  );
}
