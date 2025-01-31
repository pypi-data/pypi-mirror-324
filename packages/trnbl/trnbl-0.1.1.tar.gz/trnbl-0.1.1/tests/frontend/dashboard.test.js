// tests/frontend/dashboard.test.js

// Import the modules from your source file
import { DataManager, LayoutManager, PlotManager, IOManager } from '../../trnbl/loggers/local/frontend_src/dashboard';

// Mock external libraries
jest.mock('plotly.js-dist-min', () => ({
  newPlot: jest.fn(),
  react: jest.fn(),
}));
jest.mock('ag-grid-community', () => ({
  Grid: jest.fn(),
}));
jest.mock('feather-icons', () => ({
  replace: jest.fn(),
}));

describe('DataManager', () => {
  let dataManager;

  beforeEach(() => {
    dataManager = new DataManager();
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        text: () => Promise.resolve('{"project": "test", "metric_names": ["metric1", "metric2"]}'),
        json: () => Promise.resolve({project: "test", metric_names: ["metric1", "metric2"]}),
      })
    );
  });

  test('loadManifest should populate manifest and metricNames', async () => {
    await dataManager.loadManifest();
    expect(dataManager.manifest).toBeDefined();
    expect(dataManager.metricNames.size).toBe(2);
    expect(dataManager.projectName).toBe('test');
  });
});

describe('LayoutManager', () => {
  let layoutManager;

  beforeEach(() => {
    layoutManager = new LayoutManager('testProject');
  });

  test('get_default_layout should return correct layout', () => {
    const plotNames = ['metric1', 'metric2'];
    const layout = layoutManager.get_default_layout(plotNames);
    expect(layout).toHaveProperty('plotContainer-metric1');
    expect(layout).toHaveProperty('plotContainer-metric2');
    expect(layout).toHaveProperty('runsManifest');
  });
});

describe('PlotManager', () => {
  let plotManager;

  beforeEach(() => {
    plotManager = new PlotManager();
    document.body.innerHTML = '<div id="rootContainerDiv"></div>';
  });

  test('createPlot should add a new plot', async () => {
    await plotManager.createPlot('testMetric');
    expect(plotManager.plots).toHaveProperty('testMetric');
  });
});

describe('IOManager', () => {
  let ioManager;

  beforeEach(() => {
    ioManager = new IOManager();
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({key: 'value'}),
      })
    );
  });

  test('fetchJson should return parsed JSON', async () => {
    const result = await ioManager.fetchJson('test.json');
    expect(result).toEqual({key: 'value'});
  });
});