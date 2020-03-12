
|Etapa 1 - Captura da montagem  | 
| --- | 
|Salva as imagens diferentes durante a gravação do videos|

Primeiramente execute o comando pelo terminal dentro da pasta desejada, para baixar o projeto:
~~~ shell command
git clone https://github.com/wagner1986/build-dataset-cnn.git
~~~

Entre na pasta do projeto e  execute os seguintes comandos no terminal:
~~~ shell command
cd build-dataset-cnn
conda env list               (deve aparecer o ambiente condor37 listado)
conda activate condor37          
python cv_util.py
~~~

Abrirá 2 janelas para visualizar o que esta sendo gravado, favor deixar somente uma câmera conectada ao PC.

- Grave pelo menos de duas à três cada montagem de kit, visando obter todas as variações da montagem.
- Após a inclusão de cada elemento do kit, aguarde 1 segundo com o objetivo de capturar os elementos 
sem a mão do operador no kit.

- Após a Captura do processo de montagem dos Kits , teremos todas as imagens na pasta "/data/seg", 
movimente as que desejamos utilizar na fase de treinamento para a pasta "/images".

- Observe se o conjunto de imagens captura representa todos os momentos que desejamos identificar algo.


|Etapa 2 - OpenLabeling  | 
| --- | 
|Construiremos uma caixa envolvente para cada objeto, visando gerar o conjuto de treinamento desejado |

Baseado no repositorio: https://github.com/Cartucho/OpenLabeling
 
Segue os atalhos para utilizar a aplicação OpenLabeling: 

| Key | Description |
| --- | --- |
| h | help |
| q | quit |
| e | edges |
| a/d | previous/next image |
| s/w | previous/next class |


Mouse:
  - Use two separate left clicks to do each bounding box
  - Use the middle mouse to zoom in and out
  - Use double click to select a bounding box
  - Right click to quickly delete a bounding box

Para iniciar essa etapa execute no terminal:
~~~ shell command
python run.py --format='voc' --sort
~~~ 

O formarto gerardo com o app, é o do yolo:

| box | class|
| --- | --- |
467 330 518 425 | 0
640 243 669 313 | 0
402 357 449 442 | 0


Para finalizar o processo devemos executar o comando abaixo, para transformar no formato da nossa rede:

~~~ shell command
python process.py
~~~ 

Uma vez terminado, copie :
 - a pasta images compactada.
 - o arquivo class_list.txt utilizado
 - o arquivo condor_train_data_yolo.txt
 - e o arquivo condor_data.csv