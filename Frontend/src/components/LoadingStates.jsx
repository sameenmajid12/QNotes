import '../styles/loading.css';

// Generic Loading Spinner
export function LoadingSpinner({ size = 'md', color = 'primary' }) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16'
  };

  return (
    <div className={`loading-spinner ${sizeClasses[size]} spinner-${color}`}>
      <div className="spinner-inner"></div>
    </div>
  );
}

// Button Loading State
export function LoadingButton({ children, loading, disabled, onClick, className = '', variant = 'primary' }) {
  return (
    <button 
      className={`btn btn-${variant} ${className} ${loading ? 'loading' : ''}`}
      disabled={disabled || loading}
      onClick={onClick}
    >
      {loading ? (
        <div className="btn-loading-content">
          <LoadingSpinner size="sm" color="white" />
          <span>Loading...</span>
        </div>
      ) : (
        children
      )}
    </button>
  );
}

// Content Skeleton
export function ContentSkeleton({ lines = 3, showAvatar = false }) {
  return (
    <div className="skeleton-container">
      {showAvatar && (
        <div className="skeleton-header">
          <div className="skeleton-avatar"></div>
          <div className="skeleton-meta">
            <div className="skeleton-line skeleton-title"></div>
            <div className="skeleton-line skeleton-subtitle"></div>
          </div>
        </div>
      )}
      <div className="skeleton-content">
        {Array.from({ length: lines }).map((_, index) => (
          <div 
            key={index} 
            className={`skeleton-line ${index === lines - 1 ? 'skeleton-line-short' : ''}`}
          ></div>
        ))}
      </div>
    </div>
  );
}

// Card Skeleton
export function CardSkeleton({ count = 1, showImage = false }) {
  return (
    <div className="skeleton-cards">
      {Array.from({ length: count }).map((_, index) => (
        <div key={index} className="skeleton-card">
          {showImage && <div className="skeleton-image"></div>}
          <div className="skeleton-card-content">
            <div className="skeleton-line skeleton-title"></div>
            <div className="skeleton-line skeleton-subtitle"></div>
            <div className="skeleton-line skeleton-line-short"></div>
          </div>
        </div>
      ))}
    </div>
  );
}

// Table Skeleton
export function TableSkeleton({ rows = 5, columns = 4 }) {
  return (
    <div className="skeleton-table">
      <div className="skeleton-table-header">
        {Array.from({ length: columns }).map((_, index) => (
          <div key={index} className="skeleton-table-header-cell"></div>
        ))}
      </div>
      <div className="skeleton-table-body">
        {Array.from({ length: rows }).map((_, rowIndex) => (
          <div key={rowIndex} className="skeleton-table-row">
            {Array.from({ length: columns }).map((_, colIndex) => (
              <div key={colIndex} className="skeleton-table-cell"></div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

// Page Loading Overlay
export function PageLoader({ message = "Loading..." }) {
  return (
    <div className="page-loader-overlay">
      <div className="page-loader-content">
        <LoadingSpinner size="xl" />
        <p className="page-loader-message">{message}</p>
      </div>
    </div>
  );
}

// Inline loader for content sections
export function InlineLoader({ message = "Loading..." }) {
  return (
    <div className="inline-loader">
      <LoadingSpinner size="md" />
      <span className="inline-loader-message">{message}</span>
    </div>
  );
}

// Progress bar component
export function ProgressBar({ progress, label, showPercentage = true }) {
  return (
    <div className="progress-container">
      {label && (
        <div className="progress-label-container">
          <span className="progress-label">{label}</span>
          {showPercentage && (
            <span className="progress-percentage">{Math.round(progress)}%</span>
          )}
        </div>
      )}
      <div className="progress-track">
        <div 
          className="progress-bar-fill" 
          style={{ width: `${Math.max(0, Math.min(100, progress))}%` }}
        >
          <div className="progress-shimmer"></div>
        </div>
      </div>
    </div>
  );
}

// Error boundary fallback
export function ErrorFallback({ error, resetError }) {
  return (
    <div className="error-fallback">
      <div className="error-icon">⚠️</div>
      <h3 className="error-title">Something went wrong</h3>
      <p className="error-message">{error?.message || 'An unexpected error occurred'}</p>
      <button className="btn btn-primary" onClick={resetError}>
        Try Again
      </button>
    </div>
  );
}

// Empty state component
export function EmptyState({ 
  icon = '📭', 
  title = 'No data found', 
  description = 'There is nothing to display here yet.', 
  action = null 
}) {
  return (
    <div className="empty-state">
      <div className="empty-state-icon">{icon}</div>
      <h3 className="empty-state-title">{title}</h3>
      <p className="empty-state-description">{description}</p>
      {action && (
        <div className="empty-state-action">
          {action}
        </div>
      )}
    </div>
  );
}