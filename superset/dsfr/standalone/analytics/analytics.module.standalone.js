/*! DSFR v1.11.1 | SPDX-License-Identifier: MIT | License-Filename: LICENSE.md | restricted use (see terms and conditions) */

const config = {
  prefix: 'fr',
  namespace: 'dsfr',
  organisation: '@gouvfr',
  version: '1.11.1'
};

const api = window[config.namespace];

const ns = name => `${config.prefix}-${name}`;

ns.selector = (name, notation) => {
  if (notation === undefined) notation = '.';
  return `${notation}${ns(name)}`;
};

ns.attr = (name) => `data-${ns(name)}`;

ns.attr.selector = (name, value) => {
  let result = ns.attr(name);
  if (value !== undefined) result += `="${value}"`;
  return `[${result}]`;
};

ns.event = (type) => `${config.namespace}.${type}`;

ns.emission = (domain, type) => `emission:${domain}.${type}`;

/**
 * Copy properties from multiple sources including accessors.
 * source : https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Global_Objects/Object/assign#copier_des_accesseurs
 *
 * @param {object} [target] - Target object to copy into
 * @param {...objects} [sources] - Multiple objects
 * @return {object} A new object
 *
 * @example
 *
 *     const obj1 = {
 *        key: 'value'
 *     };
 *     const obj2 = {
 *        get function01 () {
 *          return a-value;
 *        }
 *        set function01 () {
 *          return a-value;
 *        }
 *     };
 *     completeAssign(obj1, obj2)
 */
const completeAssign = (target, ...sources) => {
  sources.forEach(source => {
    const descriptors = Object.keys(source).reduce((descriptors, key) => {
      descriptors[key] = Object.getOwnPropertyDescriptor(source, key);
      return descriptors;
    }, {});

    Object.getOwnPropertySymbols(source).forEach(sym => {
      const descriptor = Object.getOwnPropertyDescriptor(source, sym);
      if (descriptor.enumerable) {
        descriptors[sym] = descriptor;
      }
    });
    Object.defineProperties(target, descriptors);
  });
  return target;
};

class State$1 {
  constructor () {
    this.modules = {};
  }

  create (ModuleClass) {
    const module = new ModuleClass();
    this.modules[module.type] = module;
  }

  getModule (type) {
    return this.modules[type];
  }

  add (type, item) {
    this.modules[type].add(item);
  }

  remove (type, item) {
    this.modules[type].remove(item);
  }

  get isActive () {
    return this._isActive;
  }

  set isActive (value) {
    if (value === this._isActive) return;
    this._isActive = value;
    const values = Object.keys(this.modules).map((e) => {
      return this.modules[e];
    });
    if (value) {
      for (const module of values) {
        module.activate();
      }
    } else {
      for (const module of values) {
        module.deactivate();
      }
    }
  }

  get isLegacy () {
    return this._isLegacy;
  }

  set isLegacy (value) {
    if (value === this._isLegacy) return;
    this._isLegacy = value;
  }
}

const state = new State$1();

class LogLevel {
  constructor (level, light, dark, logger) {
    this.level = level;
    this.light = light;
    this.dark = dark;

    switch (logger) {
      case 'warn':
        this.logger = console.warn;
        break;

      case 'error':
        this.logger = console.error;
        break;

      default:
        this.logger = console.log;
    }
  }

  log (...values) {
    const message = new Message(config.namespace);
    for (const value of values) message.add(value);
    this.print(message);
  }

  print (message) {
    message.setColor(this.color);
    this.logger.apply(console, message.getMessage());
  }

  get color () {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? this.dark : this.light;
  }
}

class Message {
  constructor (domain) {
    this.inputs = ['%c'];
    this.styles = ['font-family:Marianne', 'line-height: 1.5'];
    this.objects = [];

    if (domain) this.add(`${domain} :`);
  }

  add (value) {
    switch (typeof value) {
      case 'object':
      case 'function':
        this.inputs.push('%o ');
        this.objects.push(value);
        break;

      default:
        this.inputs.push(`${value} `);
    }
  }

  setColor (color) {
    this.styles.push(`color:${color}`);
  }

  getMessage () {
    return [this.inputs.join(''), this.styles.join(';'), ...this.objects];
  }
}

const LEVELS = {
  log: new LogLevel(0, '#616161', '#989898'),
  debug: new LogLevel(1, '#000091', '#8B8BFF'),
  info: new LogLevel(2, '#007c3b', '#00ed70'),
  warn: new LogLevel(3, '#ba4500', '#fa5c00', 'warn'),
  error: new LogLevel(4, '#D80600', '#FF4641', 'error')
};

class Inspector {
  constructor () {
    this.level = 2;

    for (const id in LEVELS) {
      const level = LEVELS[id];
      this[id] = (...msgs) => {
        if (this.level <= level.level) level.log.apply(level, msgs);
      };
      this[id].print = level.print.bind(level);
    }
  }

  state () {
    const message = new Message();
    message.add(state);
    this.log.print(message);
  }

  tree () {
    const stage = state.getModule('stage');
    if (!stage) return;
    const message = new Message();
    this._branch(stage.root, 0, message);
    this.log.print(message);
  }

  _branch (element, space, message) {
    let branch = '';
    if (space > 0) {
      let indent = '';
      for (let i = 0; i < space; i++) indent += '    ';
      // branch += indent + '|\n';
      branch += indent + '└─ ';
    }
    branch += `[${element.id}] ${element.html}`;
    message.add(branch);
    message.add({ '@': element });
    message.add('\n');
    for (const child of element.children) branch += this._branch(child, space + 1, message);
  }
}

const inspector = new Inspector();

const startAtDomContentLoaded = (callback) => {
  if (document.readyState !== 'loading') window.requestAnimationFrame(callback);
  else document.addEventListener('DOMContentLoaded', callback);
};

const startAuto = (callback) => {
  // detect
  startAtDomContentLoaded(callback);
};

const Modes = {
  AUTO: 'auto',
  MANUAL: 'manual',
  RUNTIME: 'runtime',
  LOADED: 'loaded',
  VUE: 'vue',
  ANGULAR: 'angular',
  REACT: 'react'
};

class Options {
  constructor () {
    this._mode = Modes.AUTO;
    this.isStarted = false;
    this.starting = this.start.bind(this);
    this.preventManipulation = false;
  }

  configure (settings = {}, start, query) {
    this.startCallback = start;
    const isProduction = settings.production && (!query || query.production !== 'false');
    switch (true) {
      case query && !isNaN(query.level):
        inspector.level = Number(query.level);
        break;

      case query && query.verbose && (query.verbose === 'true' || query.verbose === 1):
        inspector.level = 0;
        break;

      case isProduction:
        inspector.level = 999;
        break;

      case settings.verbose:
        inspector.level = 0;
        break;
    }
    inspector.info(`version ${config.version}`);
    this.mode = settings.mode || Modes.AUTO;
  }

  set mode (value) {
    switch (value) {
      case Modes.AUTO:
        this.preventManipulation = false;
        startAuto(this.starting);
        break;

      case Modes.LOADED:
        this.preventManipulation = false;
        startAtDomContentLoaded(this.starting);
        break;

      case Modes.RUNTIME:
        this.preventManipulation = false;
        this.start();
        break;

      case Modes.MANUAL:
        this.preventManipulation = false;
        break;

      case Modes.VUE:
        this.preventManipulation = true;
        break;

      case Modes.ANGULAR:
        this.preventManipulation = true;
        break;

      case Modes.REACT:
        this.preventManipulation = true;
        break;

      default:
        inspector.error('Illegal mode');
        return;
    }

    this._mode = value;
    inspector.info(`mode set to ${value}`);
  }

  get mode () {
    return this._mode;
  }

  start () {
    inspector.info('start');
    this.startCallback();
  }
}

new Options();

api.inspector = completeAssign(console, {});

api.internals = {
  ns: ns
};

api.Modes = Modes;

const patch = {
  namespace: 'a4e35ba2a938ba9d007689dbf3f46acbb9807869'
};

const Collection = {
  MANUAL: 'manual',
  LOAD: 'load',
  FULL: 'full',
  HASH: 'hash'
};

const key = '_EA_';
const DISABLED = `${key}disabled`;
const TOGGLE = `${key}toggle`;

class Opt {
  constructor () {
    this._configure();
  }

  _configure () {
    const scope = this;
    window[DISABLED] = () => scope.isDisabled;
    window[TOGGLE] = this.toggle.bind(this);
  }

  get isDisabled () {
    return localStorage.getItem(key);
  }

  toggle () {
    if (this.isDisabled) this.enable();
    else this.disable();
  }

  enable () {
    if (localStorage.getItem(key)) {
      localStorage.removeItem(key);
    }
  }

  disable () {
    localStorage.setItem(key, '1');
  }
}

const opt = new Opt();

const PUSH = 'EA_push';

class Init {
  constructor (domain) {
    this._domain = domain;
    this._isLoaded = false;
    this._promise = new Promise((resolve, reject) => {
      this._resolve = resolve;
      this._reject = reject;
    });
  }

  get id () {
    return this._id;
  }

  get store () {
    return this._store;
  }

  configure () {
    this.init();
    return this._promise;
  }

  init () {
    let bit = 5381;
    for (let i = this._domain.length - 1; i > 0; i--) bit = (bit * 33) ^ this._domain.charCodeAt(i);
    bit >>>= 0;
    this._id = `_EA_${bit}`;

    this._store = [];
    this._store.eah = this._domain;
    window[this._id] = this._store;

    if (!window[PUSH]) window[PUSH] = (...args) => this.store.push(args);

    if (opt.isDisabled) {
      api.inspector.warn('User opted out, eulerian is disabled');
      this._reject('User opted out, eulerian is disabled');
    } else this.load();
  }

  load () {
    const stamp = new Date() / 1E7 | 0;
    const offset = stamp % 26;
    const key = String.fromCharCode(97 + offset, 122 - offset, 65 + offset) + (stamp % 1E3);
    this._script = document.createElement('script');
    this._script.ea = this.id;
    this._script.async = true;
    this._script.addEventListener('load', this.loaded.bind(this));
    this._script.addEventListener('error', this.error.bind(this));
    this._script.src = `//${this._domain}/${key}.js?2`;
    const node = document.getElementsByTagName('script')[0];
    node.parentNode.insertBefore(this._script, node);
  }

  error () {
    api.inspector.error('unable to load Eulerian script file. the domain declared in your configuration must match the domain provided by the Eulerian interface (tag creation)');
    this._reject('eulerian script loading error');
  }

  loaded () {
    if (this._isLoaded) return;
    this._isLoaded = true;
    this._resolve();
  }
}

/*
(function(e, a) {
  var i = e.length,
    y = 5381,
    k = 'script',
    s = window,
    v = document,
    o = v.createElement(k);
  for (; i;) {
    i -= 1;
    y = (y * 33) ^ e.charCodeAt(i)
  }
  y = '_EA_' + (y >>>= 0);
  (function(e, a, s, y) {
    s[a] = s[a] || function() {
      (s[y] = s[y] || []).push(arguments);
      s[y].eah = e;
    };
  }(e, a, s, y));
  i = new Date / 1E7 | 0;
  o.ea = y;
  y = i % 26;
  o.async = 1;
  o.src = '//' + e + '/' + String.fromCharCode(97 + y, 122 - y, 65 + y) + (i % 1E3) + '.js?2';
  s = v.getElementsByTagName(k)[0];
  s.parentNode.insertBefore(o, s);
})
('mon.domainedetracking.com', 'EA_push');
*/

/*
(function(e, a) {
  var i = e.length,
    y = 5381,
    k = 'script',
    z = '_EA_',
    zd = z + 'disabled',
    s = window,
    v = document,
    o = v.createElement(k),
    l = s.localStorage;
  for (; i;) {
    i -= 1;
    y = (y * 33) ^ e.charCodeAt(i)
  }
  y = z + (y >>>= 0);
  (function(e, a, s, y, z, zd, l) {
    s[a] = s[a] || function() {
      (s[y] = s[y] || []).push(arguments);
      s[y].eah = e;
    };
    s[zd] = function() {
      return l.getItem(z);
    };
    s[z + 'toggle'] = function() {
      (s[zd]()) ? l.removeItem(z): l.setItem(z, 1);
    }
  }(e, a, s, y, z, zd, l));
  if (!s[zd]()) {
    i = new Date / 1E7 | 0;
    o.ea = y;
    y = i % 26;
    o.async = 1;
    o.src = '//' + e + '/' + String.fromCharCode(97 + y, 122 - y, 65 + y) + (i % 1E3) + '.js?2';
    s = v.getElementsByTagName(k)[0];
    s.parentNode.insertBefore(o, s);
  }
})('mon.domainedetracking.com', 'EA_push');
*/

const State = {
  UNKNOWN: -1,
  CONFIGURING: 0,
  CONFIGURED: 1,
  INITIATED: 2,
  READY: 3
};

class TarteAuCitronIntegration {
  constructor (config) {
    this._config = config;
    this._state = State.UNKNOWN;
    this._promise = new Promise((resolve, reject) => {
      this._resolve = resolve;
      this._reject = reject;
    });
  }

  configure () {
    if (this._state >= State.CONFIGURED) return this._promise;
    if (this._state === State.UNKNOWN) {
      api.inspector.info('analytics configures tarteaucitron');
      this._state = State.CONFIGURING;
    }

    const tarteaucitron = window.tarteaucitron;
    if (!tarteaucitron || !tarteaucitron.services) {
      window.requestAnimationFrame(this.configure.bind(this));
      return;
    }

    this._state = State.CONFIGURED;
    const init = this.init.bind(this);

    const data = {
      key: 'eulerian',
      type: 'analytic',
      name: 'Eulerian Analytics',
      needConsent: true,
      cookies: ['etuix'],
      uri: 'https://eulerian.com/vie-privee',
      js: init,
      fallback: () => { tarteaucitron.services.eulerian.js(); }
    };

    tarteaucitron.services.eulerian = data;
    if (!tarteaucitron.job) tarteaucitron.job = [];
    tarteaucitron.job.push('eulerian');

    return this._promise;
  }

  init () {
    if (this._state >= State.INITIATED) return;
    this._state = State.INITIATED;
    window.__eaGenericCmpApi = this.integrate.bind(this);
    const update = this.update.bind(this);
    window.addEventListener('tac.close_alert', update);
    window.addEventListener('tac.close_panel', update);
  }

  integrate (cmpApi) {
    if (this._state >= State.READY) return;
    this._state = State.READY;
    this._cmpApi = cmpApi;

    api.inspector.info('analytics has integrated tarteaucitron');

    this._resolve();
    this.update();
  }

  update () {
    if (this._state < State.READY) return;
    this._cmpApi('tac', window.tarteaucitron, 1);
  }
}

class ConsentManagerPlatform {
  constructor (config) {
    this._config = config;

    if (config) {
      switch (config.id) {
        case 'tarteaucitron':
          this.integrateTarteAuCitron();
          break;
      }
    }
  }

  integrateTarteAuCitron () {
    this._tac = new TarteAuCitronIntegration(this._config);
    return this._tac.configure();
  }

  optin () {

  }
}

const push = (type, layer) => {
  if (typeof window.EA_push !== 'function') {
    api.inspector.warn('Analytics datalayer not sent, Eulerian API isn\'t yet avalaible');
    return;
  }

  api.inspector.info('analytics', type, layer);

  window.EA_push(type, layer);
};

const PushType = {
  COLLECTOR: 'collector',
  ACTION: 'action',
  ACTION_PARAMETER: 'actionparam'
};

class Renderer {
  constructor () {
    this._renderables = [];
    this._rendering = this.render.bind(this);
    requestAnimationFrame(this._rendering);
  }

  add (renderable) {
    const index = this._renderables.indexOf(renderable);
    if (index === -1) this._renderables.push(renderable);
  }

  remove (renderable) {
    const index = this._renderables.indexOf(renderable);
    if (index > -1) this._renderables.splice(index, 1);
  }

  render () {
    this._renderables.forEach(renderable => renderable.render());
    requestAnimationFrame(this._rendering);
  }
}

const renderer = new Renderer();

const SLICE = 80;

class Queue {
  constructor () {
    this._startingActions = [];
    this._endingActions = [];
    this._handlingVisibilityChange = this._handleVisibilityChange.bind(this);
    this._handlingEnd = this._handleEnd.bind(this);
    this._isStarted = false;
    this._isListening = false;
    this.reset();
  }

  setCollector (collector) {
    this._collector = collector;
  }

  reset (ending = false) {
    this._type = PushType.ACTION;
    if (!ending) this._startingActions.length = 0;
    this._endingActions.length = 0;
    this._count = 0;
    this._delay = -1;
    this._isRequested = false;
    this._unlisten();
  }

  start () {
    if (this._isStarted) return;
    this._isStarted = true;
    renderer.add(this);
  }

  collect () {
    this._type = PushType.COLLECTOR;
    this._request();
  }

  appendStartingAction (action, data) {
    if (!this._collector.isActionEnabled && !action.isForced) return;
    if (!action || this._startingActions.some(queued => queued.test(action))) {
      api.inspector.log('appendStartingAction exists or null', action);
      return;
    }
    const queued = new QueuedAction(action, data);
    this._startingActions.push(queued);
    this._request();
  }

  appendEndingAction (action, data) {
    if (!this._collector.isActionEnabled && !action.isForced) return;
    if (!action || this._endingActions.some(queued => queued.test(action))) {
      api.inspector.log('appendEndingAction exists or null', action);
      return;
    }
    const queued = new QueuedAction(action, data);
    this._endingActions.push(queued);
    this._request();
  }

  _request () {
    this._listen();
    this._isRequested = true;
    this._delay = 4;
  }

  _listen () {
    if (this._isListening) return;
    this._isListening = true;
    document.addEventListener('visibilitychange', this._handlingVisibilityChange);
    document.addEventListener('unload', this._handlingEnd);
    document.addEventListener('beforeunload', this._handlingEnd);
    document.addEventListener('pagehide', this._handlingEnd);
  }

  _unlisten () {
    if (!this._isListening) return;
    this._isListening = false;
    document.removeEventListener('visibilitychange', this._handlingVisibilityChange);
    document.removeEventListener('unload', this._handlingEnd);
    document.removeEventListener('beforeunload', this._handlingEnd);
    document.removeEventListener('pagehide', this._handlingEnd);
  }

  _handleVisibilityChange (e) {
    if (document.visibilityState === 'hidden') this.send();
  }

  _handleEnd () {
    this.send();
  }

  render () {
    if (this._delay <= -1) return;
    this._delay--;
    this._count++;
    switch (true) {
      case this._count > 20:
      case this._delay === 0:
        this.send();
        break;
    }
  }

  send (ending = false) {
    if (!this._isRequested) return;
    const actionLayers = [];
    if (!ending) actionLayers.push(...this._startingActions.map(queued => queued.start()).filter(layer => layer.length > 0));
    actionLayers.push(...this._endingActions.map(queued => queued.end()).filter(layer => layer.length > 0));

    const length = ((actionLayers.length / SLICE) + 1) | 0;
    const slices = [];
    for (let i = 0; i < length; i++) {
      const slice = actionLayers.slice(i * SLICE, (i + 1) * SLICE);
      slices.push(slice.flat());
    }

    if (this._type === PushType.COLLECTOR && this._collector.isCollecting) {
      const layer = this._collector.layer;
      if (slices.length > 0) {
        const slice = slices.splice(0, 1)[0];
        if (slice.length > 0) layer.push.apply(layer, slice);
      }
      layer.flat();
      if (layer.length > 0) push(PushType.COLLECTOR, layer);
    }

    if (slices.length > 0) {
      for (let i = 0; i < slices.length; i++) {
        const slice = slices[i];
        if (slice.length > 0) push(PushType.ACTION, slice);
      }
    }

    this.reset(ending);
  }
}

class QueuedAction {
  constructor (action, data) {
    this._action = action;
    this._data = data;
  }

  test (action) {
    return this._action === action;
  }

  start () {
    return this._action.start(this._data);
  }

  end () {
    return this._action.end(this._data);
  }
}

const queue = new Queue();

class Debug {
  get debugger () {
    return window._oEa;
  }

  get isActive () {
    if (!this.debugger) return false;
    return this.debugger._dbg === '1';
  }

  set isActive (value) {
    if (!this.debugger || this.isActive === value) return;
    this.debugger.debug(value ? 1 : 0);
  }
}

const debug = new Debug();

const Status = {
  CONNECTED: {
    id: 'connected',
    value: 'connecté',
    isConnected: true,
    isDefault: true
  },
  ANONYMOUS: {
    id: 'anonymous',
    value: 'anonyme',
    isConnected: false,
    isDefault: true
  },
  GUEST: {
    id: 'guest',
    value: 'invité',
    isConnected: false
  }
};

const Type = {
  INDIVIDUAL: {
    id: 'individual',
    value: 'part'
  },
  PROFESSIONNAL: {
    id: 'professionnal',
    value: 'pro'
  }
};

/*  '["\'<>*$&~`|\\\\?^~]'; */
var RESTRICTED = {
  '0x0022': '＂',
  '0x0024': '＄',
  '0x0026': '＆',
  '0x0027': '＇',
  '0x002a': '＊',
  '0x002c': '，',
  '0x003c': '＜',
  '0x003e': '＞',
  '0x003f': '？',
  '0x005c': '＼',
  '0x005e': '＾',
  '0x0060': '｀',
  '0x007c': '｜',
  '0x007e': '～'
};

// import TABLE from './unicode-table';

const charCodeHex = (char) => {
  const code = char.charCodeAt(0).toString(16);
  return '0x0000'.slice(0, -code.length) + code;
};

const normalize = (text) => {
  if (!text) return text;
  // text = [...text].map(char => TABLE[charCodeHex(char)] || char).join('');
  text = [...text].map(char => RESTRICTED[charCodeHex(char)] || char).join('');
  text = text.replace(/\s+/g, ' ').replace(/\s/g, '_');
  text = text.toLowerCase();
  return text;
};

const validateString = (value, name, allowNull = true) => {
  switch (true) {
    case typeof value === 'number':
      return `${value}`;

    case typeof value === 'string':
      return value;

    case value === undefined && allowNull:
    case value === null && allowNull:
      return '';
  }

  api.inspector.warn(`unexpected value '${value}' set at analytics.${name}. Expecting a String`);
  return null;
};

const validateNumber = (value, name, allowNull = true) => {
  switch (true) {
    case !isNaN(value):
      return value;

    case typeof value === 'string' && !isNaN(Number(value)):
      return Number(value);

    case value === undefined && allowNull:
    case value === null && allowNull:
      return -1;
  }

  api.inspector.warn(`unexpected value '${value}' set at analytics.${name}. Expecting a Number`);
  return null;
};

const validateBoolean = (value, name) => {
  switch (true) {
    case typeof value === 'boolean':
      return value;

    case typeof value === 'string' && value.toLowerCase() === 'true':
    case value === '1':
    case value === 1:
      return true;

    case typeof value === 'string' && value.toLowerCase() === 'false':
    case value === '0':
    case value === 0:
      return false;

    case value === undefined:
    case value === null:
      return value;
  }

  api.inspector.warn(`unexpected value '${value}' set at analytics.${name}. Expecting a Boolean`);
  return null;
};

const validateLang = (value, name, allowNull = true) => {
  switch (true) {
    case typeof value === 'string' && /^[A-Za-z]{2}$|^[A-Za-z]{2}[-_]/.test(value):
      return value.split(/[-_]/)[0].toLowerCase();

    case value === undefined && allowNull:
    case value === null && allowNull:
      return '';
  }

  api.inspector.warn(`unexpected value '${value}' set at analytics.${name}. Expecting language as a String following ISO 639-1 format`);
  return null;
};

const validateGeography = (value, name, allowNull = true) => {
  switch (true) {
    case typeof value === 'string':
      if (!/^FR-[A-Z0-9]{2,3}$/.test(value)) api.inspector.warn(`value '${value}' set at analytics.${name} with wrong format. Geographic location should be a String following ISO 3166-2:FR format`);
      return value;

    case value === undefined && allowNull:
    case value === null && allowNull:
      return '';
  }

  api.inspector.warn(`unexpected value '${value}' set at analytics.${name}. Expecting geographic location as a String following ISO 3166-2:FR format`);
  return null;
};

const normaliseISODate = (date) => date.toISOString().split('T')[0];

const validateDate = (value, name, allowNull = true) => {
  switch (true) {
    case value instanceof Date:
      return normaliseISODate(value);

    case typeof value === 'string': {
      const date = new Date(value);
      if (date.toString() !== 'Invalid Date') return normaliseISODate(date);
      break;
    }

    case value === undefined && allowNull:
    case value === null && allowNull:
      return null;
  }

  api.inspector.warn(`unexpected value '${value}' set at analytics.${name}. Expecting a Date`);
  return null;
};

class User {
  constructor (config) {
    this._config = config || {};
  }

  reset (clear = false) {
    this._isConnected = false;
    this.status = Status.ANONYMOUS;
    if (!clear && this._config.connect) this.connect(this._config.connect.uid, this._config.connect.email, this._config.connect.isNew);
    else {
      this._uid = undefined;
      this._email = undefined;
      this._isNew = false;
    }
    this.profile = clear ? undefined : this._config.profile;
    this.language = clear ? undefined : this._config.language;
    this.type = clear ? undefined : this._config.type;
  }

  connect (uid, email, isNew = false) {
    this._uid = validateString(uid, 'user.uid');
    if (/^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~.-]{2,}@[a-zA-Z0-9-]{2,}\.[a-zA-Z]{2,}$/.test(email)) api.inspector.warn('Please check analytics.user.email is properly encrypted ');
    this._email = validateString(email, 'user.email');
    this._isNew = validateBoolean(isNew);
    this._isConnected = true;
    this.status = Status.CONNECTED;
  }

  get uid () {
    return this._uid;
  }

  get email () {
    return this._email;
  }

  get isNew () {
    return this._isNew;
  }

  set status (id) {
    const stati = Object.values(Status).filter(status => status.isConnected === this._isConnected);
    this._status = stati.filter(status => status.id === id || status.value === id)[0] || stati.filter(status => status.isDefault)[0];
  }

  get status () {
    return this._status.id;
  }

  set profile (value) {
    const valid = validateString(value, 'user.profile');
    if (valid !== null) this._profile = valid;
  }

  get profile () {
    return this._profile.id;
  }

  set language (value) {
    const valid = validateLang(value, 'user.language');
    if (valid !== null) this._language = valid;
  }

  get language () {
    return this._language || navigator.language;
  }

  set type (id) {
    this._type = Object.values(Type).filter(type => type.id === id || type.value === id)[0];
  }

  get type () {
    return this._type.id;
  }

  get layer () {
    const layer = [];
    if (this.uid) layer.push('uid', normalize(this.uid));
    if (this.email) layer.push('email', normalize(this.email));
    if (this.isNew) layer.push('newcustomer', '1');
    if (this.language) layer.push('user_language', this.language);
    layer.push('user_login_status', this._status.value);
    if (this._profile) layer.push('profile', this._profile);
    if (this._type) layer.push('user_type', this._type.value);
    return layer;
  }
}

User.Status = Status;
User.Type = Type;

const Environment = {
  DEVELOPMENT: {
    id: 'development',
    value: 'dev'
  },
  STAGE: {
    id: 'stage',
    value: 'stage'
  },
  PRODUCTION: {
    id: 'production',
    value: 'prod'
  }
};

class Site {
  constructor (config) {
    this._config = config || {};
  }

  reset (clear = false) {
    this.environment = clear ? Environment.DEVELOPMENT.id : this._config.environment;
    this.entity = clear ? undefined : this._config.entity;
    this.language = clear ? undefined : this._config.language;
    this.target = clear ? undefined : this._config.target;
    this.type = clear ? undefined : this._config.type;
    this.region = clear ? undefined : this._config.region;
    this.department = clear ? undefined : this._config.department;
    this.version = clear ? undefined : this._config.version;
    this._api = api.version;
  }

  set environment (value) {
    switch (value) {
      case Environment.PRODUCTION.id:
      case Environment.PRODUCTION.value:
        this._environment = Environment.PRODUCTION;
        break;

      case Environment.STAGE.id:
      case Environment.STAGE.value:
        this._environment = Environment.STAGE;
        break;

      case Environment.DEVELOPMENT.id:
      case Environment.DEVELOPMENT.value:
        this._environment = Environment.DEVELOPMENT;
        break;

      default:
        this._environment = Environment.DEVELOPMENT;
    }
  }

  get environment () {
    return this._environment ? this._environment.id : Environment.DEVELOPMENT.id;
  }

  set entity (value) {
    const valid = validateString(value, 'site.entity');
    if (valid !== null) this._entity = valid;
  }

  get entity () {
    return this._entity;
  }

  set language (value) {
    const valid = validateLang(value, 'site.language');
    if (valid !== null) this._language = valid;
  }

  get language () {
    return this._language || document.documentElement.lang;
  }

  set target (value) {
    const valid = validateString(value, 'site.target');
    if (valid !== null) this._target = valid;
  }

  get target () {
    return this._target;
  }

  set type (value) {
    const valid = validateString(value, 'site.type');
    if (valid !== null) this._type = valid;
  }

  get type () {
    return this._type;
  }

  set region (value) {
    const valid = validateGeography(value, 'site.region');
    if (valid !== null) this._region = valid;
  }

  get region () {
    return this._region;
  }

  set department (value) {
    const valid = validateGeography(value, 'site.department');
    if (valid !== null) this._department = valid;
  }

  get department () {
    return this._department;
  }

  set version (value) {
    const valid = validateString(value, 'site.version');
    if (valid !== null) this._version = valid;
  }

  get version () {
    return this._version;
  }

  get api () {
    return this._api;
  }

  get layer () {
    const layer = [];
    layer.push('site_environment', this._environment.value);
    if (this.entity) layer.push('site_entity', normalize(this.entity));
    else api.inspector.warn('entity is required in analytics.site');
    if (this.language) layer.push('site_language', this.language);
    if (this.target) layer.push('site_target', normalize(this.target));
    if (this.type) layer.push('site_type', normalize(this.type));
    if (this.region) layer.push('site_region', this.region);
    if (this.department) layer.push('site_department', this.department);
    if (this.version) layer.push('site_version', this.version);
    if (this.api) layer.push('api_version', this.api);
    return layer;
  }
}

Site.Environment = Environment;

const Inventory = {
  accordion: api.internals.ns.selector('accordion'),
  alert: api.internals.ns.selector('alert'),
  badge: api.internals.ns.selector('badge'),
  breadcrumb: api.internals.ns.selector('breadcrumb'),
  button: api.internals.ns.selector('btn'),
  callout: api.internals.ns.selector('callout'),
  card: api.internals.ns.selector('card'),
  checkbox: api.internals.ns.selector('checkbox-group'),
  connect: api.internals.ns.selector('connect'),
  consent: api.internals.ns.selector('consent-banner'),
  content: api.internals.ns.selector('content-media'),
  download: api.internals.ns.selector('download'),
  follow: api.internals.ns.selector('follow'),
  footer: api.internals.ns.selector('footer'),
  header: api.internals.ns.selector('header'),
  highlight: api.internals.ns.selector('highlight'),
  input: api.internals.ns.selector('input-group'),
  link: api.internals.ns.selector('link'),
  modal: api.internals.ns.selector('modal'),
  navigation: api.internals.ns.selector('nav'),
  notice: api.internals.ns.selector('notice'),
  pagination: api.internals.ns.selector('pagination'),
  quote: api.internals.ns.selector('quote'),
  radio: api.internals.ns.selector('radio-group'),
  search: api.internals.ns.selector('search-bar'),
  select: api.internals.ns.selector('select'),
  share: api.internals.ns.selector('share'),
  sidemenu: api.internals.ns.selector('sidemenu'),
  stepper: api.internals.ns.selector('stepper'),
  summary: api.internals.ns.selector('summary'),
  tab: api.internals.ns.selector('tabs'),
  table: api.internals.ns.selector('table'),
  tag: api.internals.ns.selector('tag'),
  tile: api.internals.ns.selector('tile'),
  toggle: api.internals.ns.selector('toggle'),
  tooltip: api.internals.ns.selector('tooltip'),
  transcription: api.internals.ns.selector('transcription'),
  translate: api.internals.ns.selector('translate'),
  upload: api.internals.ns.selector('upload-group')
};

const CollectionState = {
  COLLECTABLE: 'collectable',
  COLLECTING: 'collecting',
  COLLECTED: 'collected'
};

class Page {
  constructor (config) {
    this._config = config || {};
    this._state = CollectionState.COLLECTABLE;
  }

  reset (clear = false) {
    this.path = clear ? '' : this._config.path;
    this.referrer = clear ? '' : this._config.referrer;
    this.title = clear ? '' : this._config.title;
    this.name = clear ? '' : this._config.name;
    this.id = clear ? '' : this._config.id;
    this.author = clear ? '' : this._config.author;
    this.date = clear ? '' : this._config.date;
    this._labels = clear || !this._config.labels ? ['', '', '', '', ''] : this._config.labels;
    this._labels.length = 5;
    this._tags = clear || !this._config.tags ? [] : this._config.tags;
    this._categories = clear || !this._config.categories ? ['', '', ''] : this._config.categories;
    this.isError = !clear && this._config.isError;
    this.template = clear ? '' : this._config.template;
    this.group = clear ? '' : this._config.group;
    this.segment = clear ? '' : this._config.segment;
    this.subtemplate = clear ? '' : this._config.subtemplate;
    this.theme = clear ? '' : this._config.theme;
    this.subtheme = clear ? '' : this._config.subtheme;
    this.related = clear ? '' : this._config.related;
    this.depth = clear || isNaN(this._config.depth) ? 0 : this._config.depth;
    this.current = clear || isNaN(this._config.current) ? -1 : this._config.current;
    this.total = clear || isNaN(this._config.total) ? -1 : this._config.total;
    this._filters = clear || !this._config.filters ? [] : this._config.filters;
  }

  collecting () {
    if (this._state !== CollectionState.COLLECTABLE) {
      api.inspector.warn(`current path '${this.path}' was already collected`);
      return false;
    }
    this._state = CollectionState.COLLECTING;
    return true;
  }

  get isCollecting () {
    return this._state === CollectionState.COLLECTING;
  }

  set path (value) {
    const valid = validateString(value, 'page.path');
    if (valid !== null) {
      this._path = valid;
      this._state = CollectionState.COLLECTABLE;
    }
  }

  get path () {
    return this._path || `${document.location.pathname}${document.location.search}`;
  }

  set referrer (value) {
    const valid = validateString(value, 'page.referrer');
    if (valid !== null) this._referrer = valid;
  }

  get referrer () {
    return this._referrer;
  }

  set title (value) {
    const valid = validateString(value, 'page.title');
    if (valid !== null) this._title = valid;
  }

  get title () {
    return this._title || document.title;
  }

  set id (value) {
    const valid = validateString(value, 'page.id');
    if (valid !== null) this._id = valid;
  }

  get id () {
    return this._id;
  }

  set author (value) {
    const valid = validateString(value, 'page.author');
    if (valid !== null) this._author = valid;
  }

  get author () {
    return this._author;
  }

  set date (value) {
    const valid = validateDate(value, 'page.date');
    if (valid !== null) this._date = valid;
  }

  get date () {
    return this._date;
  }

  get tags () {
    return this._tags;
  }

  set name (value) {
    const valid = validateString(value, 'page.name');
    if (valid !== null) this._name = valid;
  }

  get name () {
    return this._name || this.title;
  }

  get labels () {
    return this._labels;
  }

  get categories () {
    return this._categories;
  }

  set isError (value) {
    const valid = validateBoolean(value, 'page.isError');
    if (valid !== null) this._isError = valid;
  }

  get isError () {
    return this._isError;
  }

  set template (value) {
    const valid = validateString(value, 'page.template');
    if (valid !== null) this._template = valid;
  }

  get template () {
    return this._template || 'autres';
  }

  set segment (value) {
    const valid = validateString(value, 'page.segment');
    if (valid !== null) this._segment = valid;
  }

  get segment () {
    return this._segment || this.template;
  }

  set group (value) {
    const valid = validateString(value, 'page.group');
    if (valid !== null) this._group = valid;
  }

  get group () {
    return this._group || this.template;
  }

  set subtemplate (value) {
    const valid = validateString(value, 'page.subtemplate');
    if (valid !== null) this._subtemplate = valid;
  }

  get subtemplate () {
    return this._subtemplate;
  }

  set theme (value) {
    const valid = validateString(value, 'page.theme');
    if (valid !== null) this._theme = valid;
  }

  get theme () {
    return this._theme;
  }

  set subtheme (value) {
    const valid = validateString(value, 'page.subtheme');
    if (valid !== null) this._subtheme = valid;
  }

  get subtheme () {
    return this._subtheme;
  }

  set related (value) {
    const valid = validateString(value, 'page.related');
    if (valid !== null) this._related = valid;
  }

  get related () {
    return this._related;
  }

  set depth (value) {
    const valid = validateNumber(value, 'page.depth');
    if (valid !== null) this._depth = valid;
  }

  get depth () {
    return this._depth;
  }

  set current (value) {
    const valid = validateNumber(value, 'page.current');
    if (valid !== null) this._current = valid;
  }

  get current () {
    return this._current;
  }

  set total (value) {
    const valid = validateNumber(value, 'page.total');
    if (valid !== null) this._total = valid;
  }

  get total () {
    return this._total;
  }

  get filters () {
    return this._filters;
  }

  get layer () {
    this._state = CollectionState.COLLECTED;
    const layer = [];
    if (this.path) layer.push('path', normalize(this.path));
    if (this.referrer) layer.push('referrer', normalize(this.referrer));
    if (this.title) layer.push('page_title', normalize(this.title));
    if (this.name) layer.push('page_name', normalize(this.name));
    if (this.id) layer.push('page_id', normalize(this.id));
    if (this.author) layer.push('page_author', normalize(this.author));
    if (this.date) layer.push('page_date', normalize(this.date));

    const components = Object.keys(Inventory).map(id => document.querySelector(Inventory[id]) !== null ? id : null).filter(id => id !== null).join(',');
    if (components) layer.push('page_components', components);

    const labels = this._labels.slice(0, 5);
    labels.length = 5;
    if (labels.some(label => label)) layer.push('pagelabel', labels.map(label => typeof label === 'string' ? normalize(label) : '').join(','));

    const tags = this._tags;
    if (tags.some(tag => tag)) layer.push('pagetag', tags.map(tag => typeof tag === 'string' ? normalize(tag) : '').join(','));

    this._categories.forEach((category, index) => {
      if (category) layer.push(`page_category${index + 1}`, category);
    });

    if (this._isError) layer.push('error', '1');

    layer.push('page_template', normalize(this.template));
    layer.push('pagegroup', normalize(this.group));
    layer.push('site-segment', normalize(this.segment));

    if (this.subtemplate) layer.push('page_subtemplate', normalize(this.subtemplate));
    if (this.theme) layer.push('page_theme', normalize(this.theme));
    if (this.subtheme) layer.push('page_subtheme', normalize(this.subtheme));
    if (this.related) layer.push('page_related', normalize(this.related));
    if (!isNaN(this.depth)) layer.push('page_depth', this.depth);

    if (!isNaN(this.current) && this.current > -1) {
      let pagination = `${this.current}`;
      if (!isNaN(this.total) && this.total > -1) pagination += `/${this.total}`;
      layer.push('page_pagination', pagination);
    }

    if (this.filters.length && this.filters.some(label => label)) {
      const filters = this.filters.map(filter => typeof filter === 'string' ? normalize(filter) : '');
      layer.push('page_filters', filters.join(','));
    }
    return layer;
  }
}

const Method = {
  STANDARD: {
    id: 'standard',
    value: 'standard',
    isDefault: true
  },
  AUTOCOMPLETE: {
    id: 'autocomplete',
    value: 'autocompletion'
  }
};

class Search {
  constructor (config) {
    this._config = config || {};
  }

  reset (clear = false) {
    this.engine = clear ? undefined : this._config.engine;
    this.results = clear || isNaN(this._config.results) ? -1 : this._config.results;
    this.terms = clear ? undefined : this._config.terms;
    this.category = clear ? undefined : this._config.category;
    this.theme = clear ? undefined : this._config.theme;
    this.type = clear ? undefined : this._config.type;
    this.method = clear ? undefined : this._config.method;
  }

  set engine (value) {
    const valid = validateString(value, 'search.engine');
    if (valid !== null) this._engine = valid;
  }

  get engine () {
    return this._engine;
  }

  set results (value) {
    const valid = validateNumber(value, 'search.results');
    if (valid !== null) this._results = valid;
  }

  get results () {
    return this._results;
  }

  set terms (value) {
    const valid = validateString(value, 'search.terms');
    if (valid !== null) this._terms = valid;
  }

  get terms () {
    return this._terms;
  }

  set category (value) {
    const valid = validateString(value, 'search.category');
    if (valid !== null) this._category = valid;
  }

  get category () {
    return this._category;
  }

  set theme (value) {
    const valid = validateString(value, 'search.theme');
    if (valid !== null) this._theme = valid;
  }

  get theme () {
    return this._theme;
  }

  set type (value) {
    const valid = validateString(value, 'search.type');
    if (valid !== null) this._type = valid;
    this._type = value;
  }

  get type () {
    return this._type;
  }

  set method (id) {
    const methods = Object.values(Method);
    this._method = methods.filter(method => method.id === id || method.value === id)[0] || methods.filter(method => method.isDefault)[0];
  }

  get method () {
    return this._method;
  }

  get layer () {
    const layer = [];
    if (this.engine) layer.push('isearchengine', normalize(this.engine));
    if (this.results > -1) layer.push('isearchresults', this.results);
    if (this.terms) layer.push('isearchkey', 'search_terms', 'isearchdata', normalize(this.terms));
    if (this.category) layer.push('isearchkey', 'search_category', 'isearchdata', normalize(this.category));
    if (this.theme) layer.push('isearchkey', 'search_theme', 'isearchdata', normalize(this.theme));
    if (this.type) layer.push('isearchkey', 'search_type', 'isearchdata', normalize(this.type));
    if (this._method && layer.length) layer.push('isearchkey', 'search_method', 'isearchdata', this._method.value);
    return layer;
  }
}

Search.Method = Method;

class Funnel {
  constructor (config) {
    this._config = config || {};
  }

  reset (clear = false) {
    this.id = clear ? undefined : this._config.id;
    this.type = clear ? undefined : this._config.type;
    this.name = clear ? undefined : this._config.name;
    this.step = clear ? undefined : this._config.step;
    this.current = clear || isNaN(this._config.current) ? -1 : this._config.current;
    this.total = clear || isNaN(this._config.total) ? -1 : this._config.total;
    this.objective = clear ? undefined : this._config.objective;
    this.error = clear ? undefined : this._config.error;
  }

  set id (value) {
    const valid = validateString(value, 'funnel.id');
    if (valid !== null) this._id = valid;
  }

  get id () {
    return this._id;
  }

  set type (value) {
    const valid = validateString(value, 'funnel.type');
    if (valid !== null) this._type = valid;
  }

  get type () {
    return this._type;
  }

  set name (value) {
    const valid = validateString(value, 'funnel.name');
    if (valid !== null) this._name = valid;
  }

  get name () {
    return this._name;
  }

  set step (value) {
    const valid = validateString(value, 'funnel.step');
    if (valid !== null) this._step = valid;
  }

  get step () {
    return this._step;
  }

  set current (value) {
    const valid = validateNumber(value, 'funnel.current');
    if (valid !== null) this._current = valid;
  }

  get current () {
    return this._current;
  }

  set total (value) {
    const valid = validateNumber(value, 'funnel.total');
    if (valid !== null) this._total = valid;
  }

  get total () {
    return this._total;
  }

  set objective (value) {
    const valid = validateString(value, 'funnel.objective');
    if (valid !== null) this._objective = valid;
    this._objective = value;
  }

  get objective () {
    return this._objective;
  }

  set error (value) {
    const valid = validateString(value, 'funnel.error');
    if (valid !== null) this._error = valid;
    this._error = value;
  }

  get error () {
    return this._error;
  }

  get layer () {
    const layer = [];
    if (this.id) layer.push('funnel_id', normalize(this.id));
    if (this.type) layer.push('funnel_type', normalize(this.type));
    if (this.name) layer.push('funnel_name', normalize(this.name));
    if (this.step) layer.push('funnel_step_name', normalize(this.step));
    if (!isNaN(this.current) && this.current > -1) layer.push('funnel_step_number', this.current);
    if (!isNaN(this.total) && this.total > -1) layer.push('funnel_step_max', this.total);
    if (this.objective) layer.push('funnel_objective', normalize(this.objective));
    if (this.error) layer.push('funnel_error', normalize(this.error));
    return layer;
  }
}

const ActionMode = {
  IN: 'in',
  OUT: 'out',
  NONE: 'none'
};

const ActionStatus = {
  UNSTARTED: {
    id: 'unstarted',
    value: -1
  },
  STARTED: {
    id: 'started',
    value: 1
  },
  SINGULAR: {
    id: 'singular',
    value: 2
  },
  ENDED: {
    id: 'ended',
    value: 3
  }
};

const getParametersLayer = (data) => {
  return Object.entries(data).map(([key, value]) => ['actionpname', normalize(key), 'actionpvalue', normalize(value)]).flat();
};

class Action {
  constructor (name) {
    this._isMuted = false;
    this._isForced = false;
    this._name = name;
    this._status = ActionStatus.UNSTARTED;
    this._labels = [];
    this._parameters = {};
    this._sentData = [];
  }

  get isMuted () {
    return this._isMuted;
  }

  set isMuted (value) {
    this._isMuted = value;
  }

  get isForced () {
    return this._isForced;
  }

  set isForced (value) {
    this._isForced = value;
  }

  get isSingular () {
    return this._status === ActionStatus.SINGULAR;
  }

  get status () {
    return this._status;
  }

  get name () {
    return this._name;
  }

  get labels () {
    return this._labels;
  }

  get reference () {
    return this._reference;
  }

  get parameters () {
    return this._parameters;
  }

  get mode () {
    return this._mode;
  }

  singularize () {
    this._status = ActionStatus.SINGULAR;
  }

  rewind () {
    this._sentData = [];
    this._status = ActionStatus.UNSTARTED;
  }

  addParameter (key, value) {
    this._parameters[key] = value;
  }

  removeParameter (key) {
    delete this._parameters[key];
  }

  set reference (value) {
    const valid = validateString(value, `action ${this._name}`);
    if (valid !== null) this._reference = valid;
  }

  get _base () {
    return ['actionname', this._name];
  }

  _getLayer (data = {}) {
    if (this._isMuted) return [];

    if (this._mode !== ActionMode.IN) this._sentData.push(JSON.stringify(data));

    const layer = this._base;
    switch (this._mode) {
      case ActionMode.IN:
      case ActionMode.OUT:
        layer.push('actionmode', this._mode);
        break;
    }

    const labels = this._labels.slice(0, 5);
    labels.length = 5;
    if (labels.some(label => label)) layer.push('actionlabel', labels.map(label => typeof label === 'string' ? normalize(label) : '').join(','));

    if (this._reference) layer.push('actionref', this._reference);

    layer.push.apply(layer, getParametersLayer(Object.assign(this._parameters, data || {})));
    return layer;
  }

  start (data) {
    switch (this._status) {
      case ActionStatus.UNSTARTED:
        this._mode = ActionMode.IN;
        this._status = ActionStatus.STARTED;
        break;

      case ActionStatus.SINGULAR:
        this._mode = ActionMode.NONE;
        this._status = ActionStatus.ENDED;
        break;

      default:
        api.inspector.error(`unexpected start on action ${this._name} with status ${this._status.id}`);
        return [];
    }
    return this._getLayer(data);
  }

  end (data) {
    switch (this._status) {
      case ActionStatus.STARTED:
        this._mode = ActionMode.OUT;
        this._status = ActionStatus.ENDED;
        break;

      case ActionStatus.UNSTARTED:
        this._mode = ActionMode.NONE;
        this._status = ActionStatus.ENDED;
        break;

      case ActionStatus.SINGULAR:
        this._mode = ActionMode.NONE;
        this._status = ActionStatus.ENDED;
        break;

      case ActionStatus.ENDED:
        if (this._sentData.includes(JSON.stringify(data))) return [];
        this._mode = ActionMode.NONE;
        this._status = ActionStatus.ENDED;
        break;

      default:
        return [];
    }
    return this._getLayer(data);
  }

  resume (data) {
    if (this._isMuted) return [];
    if (this._status.value >= ActionStatus.ENDED.value) {
      api.inspector.error(`unexpected resuming on action ${this._name} with status ${this._status.id}`);
      return [];
    }
    const layer = this._base;
    if (data) layer.push.apply(layer, getParametersLayer(data));
    return layer;
  }
}

class Actions {
  constructor () {
    this._actions = [];
  }

  rewind () {
    this._actions.forEach(action => action.rewind());
  }

  getAction (name) {
    let action = this._actions.filter(action => action.name === name)[0];
    if (!action) {
      action = new Action(name);
      this._actions.push(action);
    }
    return action;
  }

  hasAction (name) {
    return this._actions.some(action => action.name === name);
  }

  remove (action) {
    const index = this._actions.indexOf(action);
    if (index === -1) return false;
    this._actions.splice(index, 1);
    return true;
  }
}

Actions.ActionMode = ActionMode;

const actions = new Actions();
Actions.instance = actions;

class Location {
  constructor (onRouteChange, isListeningHash = false) {
    this._onRouteChange = onRouteChange;
    this._isListeningHash = isListeningHash;
    this._update();
    renderer.add(this);
  }

  _update () {
    this._pathname = document.location.pathname;
    this._search = document.location.search;
    this._hash = document.location.hash;
    this._path = `${this._pathname}${this._search}`;
    if (this._isListeningHash) this._path += this._hash;
    this._hasTitle = this._title === document.title;
    this._title = document.title;
  }

  render () {
    if (this._pathname !== document.location.pathname || this._search !== document.location.search) this.change();
    if (this._isListeningHash && this._hash !== document.location.hash) this.change();
  }

  change () {
    this._referrer = this._path;
    this._update();
    this._onRouteChange();
  }

  get path () {
    return this._path;
  }

  get hasTitle () {
    return this._hasTitle;
  }

  get title () {
    return this._title;
  }

  get referrer () {
    return this._referrer;
  }
}

const CollectorEvent = {
  COLLECT: api.internals.ns.event('collect')
};

const ActioneeEmission = {
  REWIND: api.internals.ns.emission('analytics', 'rewind')
};

class Collector {
  constructor (config) {
    switch (config.collection) {
      case Collection.MANUAL:
      case Collection.LOAD:
      case Collection.FULL:
      case Collection.HASH:
        this._collection = config.collection;
        break;

      default:
        /* deprecated start */
        if (config.mode) {
          switch (config.mode) {
            case 'manual':
              this._collection = config.collection;
              break;
          }
        }
        /* deprecated end */

        switch (true) {
          /* deprecated */
          case config.mode === 'manual':
            this._collection = Collection.MANUAL;
            break;

          case api.mode === api.Modes.ANGULAR:
          case api.mode === api.Modes.REACT:
          case api.mode === api.Modes.VUE:
            this._collection = Collection.FULL;
            break;

          default:
            this._collection = Collection.LOAD;
        }
    }

    this._isActionEnabled = config.isActionEnabled === 'false' || config.isActionEnabled;

    this._user = new User(config.user);
    this._site = new Site(config.site);
    this._page = new Page(config.page);
    this._search = new Search(config.search);
    this._funnel = new Funnel(config.funnel);

    this._delay = -1;
    queue.setCollector(this);
  }

  get page () {
    return this._page;
  }

  get user () {
    return this._user;
  }

  get site () {
    return this._site;
  }

  get search () {
    return this._search;
  }

  get funnel () {
    return this._funnel;
  }

  start () {
    const handleRouteChange = this._handleRouteChange.bind(this);
    switch (this._collection) {
      case Collection.LOAD:
        this.collect();
        break;

      case Collection.FULL:
        this.collect();
        this._location = new Location(handleRouteChange);
        break;

      case Collection.HASH:
        this.collect();
        this._location = new Location(handleRouteChange, true);
        break;
    }
  }

  _handleRouteChange () {
    queue.send(true);
    this._delay = 6;
    renderer.add(this);
  }

  render () {
    this._delay--;
    if (this._delay < 0) {
      renderer.remove(this);
      this._routeChanged();
    }
  }

  _routeChanged () {
    actions.rewind();
    this._page.referrer = this._location.referrer;
    if (this._location.hasTitle) this._page.title = this._location.title;
    this._page.path = this._location.path;
    const event = new CustomEvent(CollectorEvent.COLLECT);
    document.documentElement.dispatchEvent(event);
    this.collect();
    if (api.internals && api.internals.stage && api.internals.stage.root) api.internals.stage.root.descend(ActioneeEmission.REWIND);
  }

  reset (clear = false) {
    this._user.reset(clear);
    this._site.reset(clear);
    this._page.reset(clear);
    this._search.reset(clear);
    this._funnel.reset(clear);
  }

  collect () {
    if (!this.page.collecting()) return;
    queue.collect();
  }

  get collection () {
    return this._collection;
  }

  get isCollecting () {
    return this._page.isCollecting;
  }

  get isActionEnabled () {
    return this._isActionEnabled;
  }

  set isActionEnabled (value) {
    this._isActionEnabled = value;
  }

  get layer () {
    return [
      ...this._user.layer,
      ...this._site.layer,
      ...this._page.layer,
      ...this._search.layer,
      ...this._funnel.layer
    ];
  }
}

class Analytics {
  constructor () {
    this._isReady = false;
    this._readiness = new Promise((resolve, reject) => {
      if (this._isReady) resolve();
      else {
        this._resolve = resolve;
        this._reject = reject;
      }
    });
    this._configure();
  }

  _configure () {
    switch (true) {
      case window[patch.namespace] !== undefined:
        this._config = window[patch.namespace].configuration.analytics;
        window[patch.namespace].promise.then(this._build.bind(this), () => {});
        break;

      case api.internals !== undefined && api.internals.configuration !== undefined && api.internals.configuration.analytics !== undefined && api.internals.configuration.analytics.domain !== undefined:
        this._config = api.internals.configuration.analytics;
        this._build();
        break;

      case api.analytics !== undefined && api.analytics.domain !== undefined:
        this._config = api.analytics;
        this._build();
        break;

      default:
        api.inspector.warn('analytics configuration is incorrect or missing (required : domain)');
    }
  }

  _build () {
    this._init = new Init(this._config.domain);
    this._init.configure().then(this._start.bind(this), (reason) => this._reject(reason));
  }

  get isReady () {
    return this._isReady;
  }

  get readiness () {
    return this._readiness;
  }

  _start () {
    if (this._isReady) return;

    this._cmp = new ConsentManagerPlatform(this._config.cmp);
    this._collector = new Collector(this._config);
    this._collector.reset();

    this._isReady = true;
    this._resolve();

    queue.start();
    this._collector.start();
  }

  get page () {
    return this._collector.page;
  }

  get user () {
    return this._collector.user;
  }

  get site () {
    return this._collector._site;
  }

  get search () {
    return this._collector.search;
  }

  get funnel () {
    return this._collector.funnel;
  }

  get cmp () {
    return this._cmp;
  }

  get opt () {
    return opt;
  }

  get collection () {
    return this._collector.collection;
  }

  get isActionEnabled () {
    return this._collector.isActionEnabled;
  }

  set isActionEnabled (value) {
    this._collector.isActionEnabled = value;
  }

  get isDebugging () {
    return debug.isActive;
  }

  set isDebugging (value) {
    debug.isActive = value;
  }

  push (type, layer) {
    push(type, layer);
  }

  reset (clear = false) {
    this._collector.reset();
  }

  collect () {
    this._collector.collect();
  }
}

const analytics = new Analytics();

analytics.Collection = Collection;
analytics.PushType = PushType;

api.analytics = completeAssign(analytics, {});
