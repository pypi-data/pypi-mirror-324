// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { Signal } from '@lumino/signaling';
import { Drive } from '@jupyterlab/services';
import { MyProvider } from './yprovider';
/**
 * A collaborative implementation for an `IDrive`.
 */
export class MySharedDrive extends Drive {
    /**
     * Construct a new drive object.
     *
     * @param user - The user manager to add the identity to the awareness of documents.
     */
    constructor(app, translator) {
        super({ name: 'RTC' });
        this._onCreate = (options, sharedModel) => {
            if (typeof options.format !== 'string') {
                return;
            }
            try {
                const provider = new MyProvider({
                    path: options.path,
                    format: options.format,
                    contentType: options.contentType,
                    model: sharedModel,
                    user: this._user,
                    translator: this._trans
                });
                this._app.serviceManager.contents.get(options.path, { content: true }).then(model => {
                    console.log('set model source:', model);
                    const content = model.format === 'base64' ? atob(model.content) : model.content;
                    provider.setSource(content);
                });
                const key = `${options.format}:${options.contentType}:${options.path}`;
                this._providers.set(key, provider);
                sharedModel.changed.connect(async (_, change) => {
                    var _a;
                    if (!change.stateChange) {
                        return;
                    }
                    const hashChanges = change.stateChange.filter(change => change.name === 'hash');
                    if (hashChanges.length === 0) {
                        return;
                    }
                    if (hashChanges.length > 1) {
                        console.error('Unexpected multiple changes to hash value in a single transaction');
                    }
                    const hashChange = hashChanges[0];
                    // A change in hash signifies that a save occurred on the server-side
                    // (e.g. a collaborator performed the save) - we want to notify the
                    // observers about this change so that they can store the new hash value.
                    const newPath = (_a = sharedModel.state.path) !== null && _a !== void 0 ? _a : options.path;
                    const model = await this.get(newPath, { content: false });
                    this._ydriveFileChanged.emit({
                        type: 'save',
                        newValue: { ...model, hash: hashChange.newValue },
                        // we do not have the old model because it was discarded when server made the change,
                        // we only have the old hash here (which may be empty if the file was newly created!)
                        oldValue: { hash: hashChange.oldValue }
                    });
                });
                sharedModel.disposed.connect(() => {
                    const provider = this._providers.get(key);
                    if (provider) {
                        provider.dispose();
                        this._providers.delete(key);
                    }
                });
            }
            catch (error) {
                // Falling back to the contents API if opening the websocket failed
                // This may happen if the shared document is not a YDocument.
                console.error(`Failed to open connection for ${options.path}.\n:${error}`);
            }
        };
        this._ydriveFileChanged = new Signal(this);
        this._app = app;
        this._user = app.serviceManager.user;
        this._trans = translator;
        this._providers = new Map();
        this.sharedModelFactory = new SharedModelFactory(this._onCreate);
        super.fileChanged.connect((_, change) => {
            // pass through any events from the Drive superclass
            this._ydriveFileChanged.emit(change);
        });
    }
    get providers() {
        return this._providers;
    }
    /**
     * Dispose of the resources held by the manager.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._providers.forEach(p => p.dispose());
        this._providers.clear();
        super.dispose();
    }
    /**
     * Get a file or directory.
     *
     * @param localPath: The path to the file.
     *
     * @param options: The options used to fetch the file.
     *
     * @returns A promise which resolves with the file content.
     *
     * Uses the [Jupyter Notebook API](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyter/notebook/master/notebook/services/api/api.yaml#!/contents) and validates the response model.
     */
    async get(localPath, options) {
        if (options && options.format && options.type) {
            const key = `${options.format}:${options.type}:${localPath}`;
            const provider = this._providers.get(key);
            if (provider) {
                // If the document doesn't exist, `super.get` will reject with an
                // error and the provider will never be resolved.
                // Use `Promise.all` to reject as soon as possible. The Context will
                // show a dialog to the user.
                const [model] = await Promise.all([
                    await this._app.serviceManager.contents.get(localPath, { ...options, content: false }),
                    provider.ready
                ]);
                // The server doesn't return a model with a format when content is false,
                // so set it back.
                return { ...model, format: options.format };
            }
        }
        return await this._app.serviceManager.contents.get(localPath, options);
    }
    async listCheckpoints(path) {
        return [];
    }
    /**
     * Save a file.
     *
     * @param localPath - The desired file path.
     *
     * @param options - Optional overrides to the model.
     *
     * @returns A promise which resolves with the file content model when the
     *   file is saved.
     */
    async save(localPath, options = {}) {
        // Check that there is a provider - it won't e.g. if the document model is not collaborative.
        if (options.format && options.type) {
            const key = `${options.format}:${options.type}:${localPath}`;
            const provider = this._providers.get(key);
            if (provider) {
                // Save is done from the backend
                const fetchOptions = {
                    type: options.type,
                    format: options.format,
                    content: false
                };
                return this.get(localPath, fetchOptions);
            }
        }
        return this._app.serviceManager.contents.save(localPath, options);
    }
    /**
     * A signal emitted when a file operation takes place.
     */
    get fileChanged() {
        return this._ydriveFileChanged;
    }
}
/**
 * Yjs sharedModel factory for real-time collaboration.
 */
class SharedModelFactory {
    /**
     * Shared model factory constructor
     *
     * @param _onCreate Callback on new document model creation
     */
    constructor(_onCreate) {
        this._onCreate = _onCreate;
        /**
         * Whether the IDrive supports real-time collaboration or not.
         */
        this.collaborative = true;
        this.documentFactories = new Map();
    }
    /**
     * Register a SharedDocumentFactory.
     *
     * @param type Document type
     * @param factory Document factory
     */
    registerDocumentFactory(type, factory) {
        if (this.documentFactories.has(type)) {
            throw new Error(`The content type ${type} already exists`);
        }
        this.documentFactories.set(type, factory);
    }
    /**
     * Create a new `ISharedDocument` instance.
     *
     * It should return `undefined` if the factory is not able to create a `ISharedDocument`.
     */
    createNew(options) {
        if (typeof options.format !== 'string') {
            console.warn(`Only defined format are supported; got ${options.format}.`);
            return;
        }
        if (!this.collaborative || !options.collaborative) {
            // Bail if the document model does not support collaboration
            // the `sharedModel` will be the default one.
            return;
        }
        if (this.documentFactories.has(options.contentType)) {
            const factory = this.documentFactories.get(options.contentType);
            const sharedModel = factory(options);
            this._onCreate(options, sharedModel);
            return sharedModel;
        }
        return;
    }
}
