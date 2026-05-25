import React, { useState, useEffect } from "react";
import { getSettings, saveSettings, type Settings } from "../../lib/settings";

type TimeRange = "3_months" | "6_months" | "1_year" | "all_time";

const TIME_RANGE_OPTIONS: { value: TimeRange; label: string }[] = [
  { value: "3_months", label: "Last 3 months" },
  { value: "6_months", label: "Last 6 months" },
  { value: "1_year", label: "Last year" },
  { value: "all_time", label: "All available history" },
];

export function Options() {
  const [settings, setSettings] = useState<Settings>({
    timeRange: "1_year",
    apiUrl: "http://localhost:8000",
  });
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    getSettings().then(setSettings);
  }, []);

  const handleSave = async () => {
    await saveSettings(settings);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="options">
      <header className="header">
        <h1 className="title">Chrome Wrapped Settings</h1>
      </header>

      <main className="content">
        <section className="section">
          <h2 className="section-title">Time Range</h2>
          <p className="section-description">
            Choose how far back to analyze your browsing history.
          </p>
          <div className="radio-group">
            {TIME_RANGE_OPTIONS.map((option) => (
              <label key={option.value} className="radio-label">
                <input
                  type="radio"
                  name="timeRange"
                  value={option.value}
                  checked={settings.timeRange === option.value}
                  onChange={() =>
                    setSettings({ ...settings, timeRange: option.value })
                  }
                />
                <span>{option.label}</span>
              </label>
            ))}
          </div>
        </section>

        <section className="section">
          <h2 className="section-title">Backend URL</h2>
          <p className="section-description">
            The URL of the Chrome Wrapped backend server.
          </p>
          <input
            type="url"
            className="input"
            value={settings.apiUrl}
            onChange={(e) =>
              setSettings({ ...settings, apiUrl: e.target.value })
            }
            placeholder="http://localhost:8000"
          />
        </section>

        <section className="section">
          <h2 className="section-title">Privacy</h2>
          <p className="section-description">
            Your browsing history is sent to the backend server for analysis.
            Data is automatically deleted after 24 hours. We do not share your
            data with third parties.
          </p>
        </section>

        <div className="actions">
          <button className="save-btn" onClick={handleSave}>
            {saved ? "Saved!" : "Save Settings"}
          </button>
        </div>
      </main>
    </div>
  );
}
