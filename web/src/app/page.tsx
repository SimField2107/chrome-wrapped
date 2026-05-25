import { CRTScanlines } from "@/components/retro/CRTScanlines";
import { Window98 } from "@/components/retro/Window98";

export default function HomePage() {
  return (
    <main className="landing">
      <CRTScanlines />
      <div className="landing-content">
        <Window98 title="welcome.exe">
          <div className="landing-inner">
            <h1 className="landing-title">CHROME WRAPPED</h1>
            <p className="landing-subtitle">Your year on the internet</p>

            <div className="landing-features">
              <div className="feature">
                <span className="feature-icon">📊</span>
                <h3>Website Analytics</h3>
                <p>Discover your most visited sites and browsing patterns</p>
              </div>
              <div className="feature">
                <span className="feature-icon">⏰</span>
                <h3>Time Insights</h3>
                <p>Understand your daily rhythms and peak hours</p>
              </div>
              <div className="feature">
                <span className="feature-icon">🏷️</span>
                <h3>Categories</h3>
                <p>See how you spend time across different types of sites</p>
              </div>
              <div className="feature">
                <span className="feature-icon">🧠</span>
                <h3>Personality</h3>
                <p>Discover your Browser Club and browsing persona</p>
              </div>
            </div>

            <div className="landing-cta">
              <p className="cta-text">Install the Chrome extension to get started</p>
              <div className="cta-steps">
                <div className="step">
                  <span className="step-number">1</span>
                  <span>Install Extension</span>
                </div>
                <div className="step">
                  <span className="step-number">2</span>
                  <span>Click Generate</span>
                </div>
                <div className="step">
                  <span className="step-number">3</span>
                  <span>View Your Wrapped</span>
                </div>
              </div>
            </div>
          </div>
        </Window98>
      </div>
    </main>
  );
}
