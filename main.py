import click
import kr8s

FINALIZER_NAME = "wrangler.cattle.io/klum-secret"


@click.command()
@click.option('--context', help='Kubernetes context to use.')
@click.option('--kubeconfig', default="", help='Path to the kubeconfig file to use.')
def delete_klum_secrets_finalizer(context: str, kubeconfig: str):
    client = kr8s.api(context=context, kubeconfig=kubeconfig)
    namespaces = client.get("namespaces")
    for namespace in namespaces:
        print(f"Namespace : {namespace.metadata.name}")
        secrets = client.get("secrets", namespace=namespace.metadata.name)
        for secret in secrets:
            if "finalizers" in secret.metadata and FINALIZER_NAME in secret.metadata.finalizers:
                print(f"\tPatching: {secret.metadata.name}")
                new_finalizers = [f for f in secret.metadata.finalizers if f != FINALIZER_NAME]
                secret.metadata.finalizers = new_finalizers
                secret.patch({"metadata": {"finalizers": new_finalizers}})


if __name__ == '__main__':
    delete_klum_secrets_finalizer()
