'use client';
import { usePathname, useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import Form, { IChangeEvent } from '@rjsf/core';
import jsYaml from 'js-yaml';
import validator from '@rjsf/validator-ajv8';
import { useRouter } from 'next/navigation';

export default function Page() {
  const router = useRouter(); // Get the router instance
  const pathname = usePathname();
  const step = parseInt(pathname.split('/')[2] || '1', 10);

  const [schema, setSchema] = useState({});
  const [formData, setFormData] = useState({});

  useEffect(() => {
    // Dynamically import the JSON schema based on the step
    import(`../../../schemas/schemaPage${step}.json`)
      .then(setSchema)
      .catch(console.error);

    // Retrieve saved form data from local storage
    const savedData = localStorage.getItem(`formDataStep${step}`);
    if (savedData) {
      setFormData(JSON.parse(savedData));
    }
  }, [step]);

  const onSubmit = (e: IChangeEvent<any>) => {
    const formData = e.formData;
    localStorage.setItem(`formDataStep${step}`, JSON.stringify(formData));

    if (step < 5) {
      const nextStep = step + 1;
      router.push(`/assessment/${nextStep}`); // Adjusted to use dynamic routing
    } else {
      router.push(`/report`); // Navigate to DSL page after the last step
    }
  };

  const generateDSLFromFormData = (allData) => {
    // Implement this function to convert form data to DSPyGen DSL
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
