import type { ButtonHTMLAttributes } from 'react';
import './Button.css';

type Variant = 'primary' | 'secondary' | 'tertiary' | 'accent' | 'icon';
type Size = 'md' | 'sm';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
}

export function Button({
  variant = 'primary',
  size = 'md',
  className = '',
  children,
  ...props
}: ButtonProps) {
  const classes = [
    'btn',
    variant === 'icon' ? 'btn-icon' : `btn-${variant}`,
    size === 'sm' ? 'btn-sm' : '',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <button className={classes} {...props}>
      {children}
    </button>
  );
}
