import type { InputHTMLAttributes, SelectHTMLAttributes, TextareaHTMLAttributes } from 'react';
import './Input.css';

interface FieldProps {
  label: string;
  error?: string;
}

export function Input({
  label,
  error,
  className = '',
  ...props
}: FieldProps & InputHTMLAttributes<HTMLInputElement>) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>
      <input className={`field-input ${className}`} {...props} />
      {error && <span className="field-error">{error}</span>}
    </label>
  );
}

export function Textarea({
  label,
  error,
  className = '',
  ...props
}: FieldProps & TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>
      <textarea className={`field-input field-textarea ${className}`} {...props} />
      {error && <span className="field-error">{error}</span>}
    </label>
  );
}

export function Select({
  label,
  error,
  className = '',
  children,
  ...props
}: FieldProps & SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>
      <select className={`field-input field-select ${className}`} {...props}>
        {children}
      </select>
      {error && <span className="field-error">{error}</span>}
    </label>
  );
}
