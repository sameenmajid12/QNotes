import "../styles/learn.css";

function Summary() {
  return (
    <div className="summary">
      <div className="summary-header">
        <div className="summary-title-row">
          <div>
            <h1>Apple</h1>
            <p className="summary-subtitle">
              A simplified summary of Apple's 10-Q, highlighting key metrics,
              trends, and insights.
              <br />
              Hover over terms to learn definitions and understand the numbers.
            </p>
            <div className="seperator-line"></div>
          </div>
          <button className="btn-save">Save analysis</button>
        </div>
      </div>

      <div className="summary-content">
        <div className="summary-main">
          <section className="content-section">
            <h2 className="section-heading">Key metrics at a glance</h2>
            <p className="section-text">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor <strong>incididunt</strong> ut labore et dolore
              magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
              ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute
              irure dolor in reprehenderit in <strong>voluptate</strong> velit
              esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
              occaecat <strong>cupidatat</strong> non proident, sunt in culpa
              qui officia deserunt mollit anim id est laborum.
            </p>
          </section>

          <section className="content-section">
            <h2 className="section-heading">Top insights</h2>
            <p className="section-text">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor <strong>incididunt</strong> ut labore et dolore
              magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
              ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute
              irure dolor in reprehenderit in <strong>voluptate</strong> velit
              esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
              occaecat <strong>cupidatat</strong> non proident, sunt in culpa
              qui officia deserunt mollit anim id est laborum.
            </p>
          </section>

          <section className="content-section">
            <h2 className="section-heading">Trend Highlights</h2>
            <p className="section-text">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor <strong>incididunt</strong> ut labore et dolore
              magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
              ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute
              irure dolor in reprehenderit in <strong>voluptate</strong> velit
              esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
              occaecat <strong>cupidatat</strong> non proident, sunt in culpa
              qui officia deserunt mollit anim id est laborum.
            </p>
          </section>
        </div>
        <aside className="summary-sidebar">
          <ol className="summary-toc">
            <li className="toc-item">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna
            </li>
          </ol>
        </aside>
      </div>
      <div className="cta-section">
        <p className="cta-text">
          Try to identify important trends and definitions before moving to
          Practice Mode.
        </p>
        <button className="btn-practice">
          Practice
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="10" r="8" stroke="white" strokeWidth="2" />
            <path
              d="M8 6L12 10L8 14"
              stroke="white"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
      </div>
    </div>
  );
}

export default Summary;
