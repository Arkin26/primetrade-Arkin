import type { ReactNode } from 'react';
import './Card.css';

interface CardProps {
  children: ReactNode;
  title?: string;
  subtitle?: string;
  muted?: boolean;
  className?: string;
}

export function Card({ children, title, subtitle, muted, className = '' }: CardProps) {
  return (
    <div className={`card ${muted ? 'card-muted' : ''} ${className}`}>
      {title && <h3 className="card-title">{title}</h3>}
      {subtitle && <p className="card-subtitle">{subtitle}</p>}
      {children}
    </div>
  );
}
