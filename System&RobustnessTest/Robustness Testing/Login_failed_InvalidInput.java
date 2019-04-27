package Project;


import java.util.Random;
import java.util.concurrent.TimeUnit;
import org.junit.*;
import static org.junit.Assert.*;

import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;

public class Login_failed_InvalidInput {
  private WebDriver driver;
 
  private StringBuffer verificationErrors = new StringBuffer();
  public String random_fuzzer() {
	  Random random = new Random();
	  StringBuilder builder = new StringBuilder();
	  int length = random.nextInt(99)+1;
	  for(int i = 0; i<length;i++) {
		  int n = random.nextInt(94)+33;
		  char s;
		  s=(char) n;
		  System.out.println(s);
		  builder.append(s);
		  
	  }
	  return builder.toString();
  }

  @Before
  public void setUp() throws Exception {
    driver = new FirefoxDriver();
    driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
  }


  
  @Test
  public void testInvalidInput() throws Exception {
	String user = random_fuzzer();
	String pwd= random_fuzzer();
    driver.get("http://35.198.199.181:5000/");
    driver.findElement(By.name("username")).click();
    driver.findElement(By.name("username")).clear();
    driver.findElement(By.name("username")).sendKeys(user);
    assertNotNull(user);
    assertEquals ("tom", user);
    driver.findElement(By.name("pd")).clear();
    driver.findElement(By.name("pd")).sendKeys(pwd);
    assertNotNull(pwd);
    assertEquals ("sutd1234", pwd);
    driver.findElement(By.name("pd")).sendKeys(Keys.ENTER);
    Thread.sleep(2000);
    assertEquals ("home", driver.getTitle());
  }
  
  @Test
  public void testNoInput() throws Exception {
	String user = "";
	String pwd= "";
    driver.get("http://35.198.199.181:5000/");
    driver.findElement(By.name("username")).click();
    driver.findElement(By.name("username")).clear();
    driver.findElement(By.name("username")).sendKeys(user);
    assertNotNull(user);
    assertEquals ("tom", user);
    driver.findElement(By.name("pd")).clear();
    driver.findElement(By.name("pd")).sendKeys(pwd);
    assertNotNull(pwd);
    assertEquals ("sutd1234", pwd);
    driver.findElement(By.name("pd")).sendKeys(Keys.ENTER);
    Thread.sleep(2000);
    assertEquals ("home", driver.getTitle());
  }
  
  

  @After
  public void tearDown() throws Exception {
    driver.quit();
    String verificationErrorString = verificationErrors.toString();
    if (!"".equals(verificationErrorString)) {
      fail(verificationErrorString);
    }
  }

}

