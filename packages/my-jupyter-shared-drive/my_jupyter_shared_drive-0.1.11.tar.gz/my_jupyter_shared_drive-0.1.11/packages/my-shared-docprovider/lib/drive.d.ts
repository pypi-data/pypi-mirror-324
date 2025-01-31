import { JupyterFrontEnd } from '@jupyterlab/application';
import { ISignal } from '@lumino/signaling';
import { TranslationBundle } from '@jupyterlab/translation';
import { Contents, Drive } from '@jupyterlab/services';
import { MyProvider } from './yprovider';
import { ICollaborativeDrive, ISharedModelFactory } from '@jupyter/collaborative-drive';
/**
 * A collaborative implementation for an `IDrive`.
 */
export declare class MySharedDrive extends Drive implements ICollaborativeDrive {
    /**
     * Construct a new drive object.
     *
     * @param user - The user manager to add the identity to the awareness of documents.
     */
    constructor(app: JupyterFrontEnd, translator: TranslationBundle);
    /**
     * SharedModel factory for the YDrive.
     */
    readonly sharedModelFactory: ISharedModelFactory;
    get providers(): Map<string, MyProvider>;
    /**
     * Dispose of the resources held by the manager.
     */
    dispose(): void;
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
    get(localPath: string, options?: Contents.IFetchOptions): Promise<Contents.IModel>;
    listCheckpoints(path: string): Promise<Contents.ICheckpointModel[]>;
    createCheckpoint(path: string): Promise<Contents.ICheckpointModel>;
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
    save(localPath: string, options?: Partial<Contents.IModel>): Promise<Contents.IModel>;
    /**
     * A signal emitted when a file operation takes place.
     */
    get fileChanged(): ISignal<this, Contents.IChangedArgs>;
    private _onCreate;
    private _app;
    private _user;
    private _trans;
    private _providers;
    private _ydriveFileChanged;
}
